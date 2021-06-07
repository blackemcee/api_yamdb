from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin
                    or request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_admin
                    or request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator
