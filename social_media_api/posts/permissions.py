from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit/delete it.
    Read permissions are allowed to any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an `author` attribute.
        return hasattr(obj, 'author') and obj.author == request.user
