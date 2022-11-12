from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to an administrator or a superuser.
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission allowing only an author of an object
    or a superuser to edit it.
    Assumes the model instance has an `author` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user == obj.author
            or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    """
    Object-level permission allowing only moderators
    or a superuser to edit an object.
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'moderator'
            or request.user.is_superuser
        )
