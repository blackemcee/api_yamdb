from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return ((obj.author == request.user)
                or (request.method in permissions.SAFE_METHODS))


class IsAdminOrModeratorAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role in {'admin', 'moderator'}
                    or request.user.is_superuser or obj.author == request.user)
        return request.method in permissions.SAFE_METHODS
