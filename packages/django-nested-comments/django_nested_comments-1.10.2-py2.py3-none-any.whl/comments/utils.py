from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from .models import Comment, CommentVersion

import json

class InvalidCommentException(Exception):
    """
    Throw this exception when a valid comment cannot be found/created based on the parameters of a request.
    """
    pass
    
def _get_target_comment(request):
    """
        Using parameters passed in with the request this function determines what the target comment is.
        This function returns the following tuple:
            (comment, version the user is editing (or None if new comment))
    """
    # Check if the user is attempting to edit an existing comment...
    if 'version_id' in request.POST:
        try:
            previous_version = CommentVersion.objects.select_related('comment').get(id=request.POST.get('version_id'))
            return previous_version.comment, previous_version
        except CommentVersion.DoesNotExist:
            raise InvalidCommentException("The comment you are attempting to update could not be found.")
    # Or they are trying to create a new comment...
    elif 'parent_id' in request.POST:
        try:
            parent = Comment.objects.get(id=request.POST.get('parent_id'))
            return Comment(parent=parent, created_by=request.user), None
        except Comment.DoesNotExist as e:
            raise InvalidCommentException("The comment you are responding to could not be found.")
    # Or we can't tell what they were trying to do, so we return a 404
    else:
        raise InvalidCommentException("An error occurred while saving your comment.")
    
def get_or_create_tree_root(ct_id, obj_id):
    try:
        parent_comment = None
        ct = ContentType.objects.get_for_id(ct_id)
        obj = ct.get_object_for_this_type(pk=obj_id)
        try:
            comment = Comment.objects.get(object_id=obj_id, content_type=ct)
        except Comment.DoesNotExist:
            kwargs = {}
            if hasattr(obj, 'max_comment_depth'):
                kwargs['max_depth'] = getattr(obj, 'max_comment_depth')()
            # This 'lock' ensures the creation process is done serially, since there is a built in race condition for mptt's 'tree_id' assignment
            # The issue for mptt is here: https://github.com/django-mptt/django-mptt/issues/236
            ct_lock = ContentType.objects.select_for_update().get(app_label='comments', model='comment')
            comment = Comment.objects.create(content_object=obj, **kwargs)

        # This check adds one query to every ajax call, but I decided to put it here instead of in Comment.save to ensure integrity even between saves.  
        try:
            Comment.objects.get(parent=None, tree_id=comment.tree_id)
        # If there are there are more than one 'root' comments (with no object_id) with the same tree_id...
        except Comment.MultipleObjectsReturned:
            # ...then we need to rebuild to ensure integrity
            Comment.objects.rebuild()
            
        return comment, obj
    except Exception as e:
        raise InvalidCommentException("Unable to access comment tree: parent object not found.")
    
def _get_or_create_tree_root(request):
    if 'ct_id' in request.GET and 'obj_id' in request.GET:
        return get_or_create_tree_root(request.GET.get('ct_id'), request.GET.get('obj_id'))
    else:
        raise InvalidCommentException("Unable to access comment tree: invalid request parameters.")
    
def _process_node_permissions(**kwargs):
    """
    This function checks and associates the three permissions (reply, edit, delete) to each comment node. This allows permission based access on a per comment basis.
    """
    request = kwargs.get('request', None)
    parent_object = kwargs.get('parent_object', None)
    max_depth = kwargs.get('max_depth', None)
    for comment in kwargs.get('nodes', []):
        comment.can_reply = user_has_permission(request, parent_object, 'can_reply_to_comment', comment=comment) and (comment.level < max_depth)
        comment.can_edit = user_has_permission(request, parent_object, 'can_post_comment', comment=comment)
        comment.can_delete = user_has_permission(request, parent_object, 'can_delete_comment', comment=comment)


def get_attr_val(request, obj, attr, default=None, **kwargs):
    """
    This function attempts to get a value from the 'obj' through 'attr' (either a callable or a variable). 
    If 'attr' is not defined on 'obj' then we attempt to fall back to the default.
    """
    if hasattr(obj, attr):
        attr_holder = getattr(obj, attr)
        if callable(attr_holder):
            kwargs['request'] = kwargs.get('request', request)
            kwargs['user'] = kwargs.get('user', request.user)
            return attr_holder(**kwargs)
        return attr_holder
    return default
        
def user_has_permission(request, parent_object, permission_function, **kwargs):
    """
        Helper method that defaults all permission checks to "is_authenticated" if it is not defined on the parent_object.
    """
    default = request.user.is_authenticated
    return get_attr_val(request, parent_object, permission_function, default, **kwargs)
