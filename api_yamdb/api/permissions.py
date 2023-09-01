from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Access rights for admin only."""

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Access rights only for the admin,
    for the rest only viewing is available.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )


class AuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Access rights only for the admin or author,
    for the rest only viewing is available.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin
                )
            )
        )
