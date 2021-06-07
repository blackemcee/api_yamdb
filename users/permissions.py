from rest_framework import permissions


class UserPermision(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user == obj)

    def has_permission(self, request, view):
        permission = request.user.is_authenticated
        if view.kwargs.get('username') == 'me':
            return permission
        else:
            return permission and request.user.is_admin
