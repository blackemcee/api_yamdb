from rest_framework import permissions


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsAdminOrDeny(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser)

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser)

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser)


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


class IsAdminOrModeratorAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role in {'admin', 'moderator'}
                    or request.user.is_superuser or obj.author == request.user)
        return request.method in permissions.SAFE_METHODS
