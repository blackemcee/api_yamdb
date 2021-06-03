from rest_framework import permissions


class IsAdminOrDeny(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser
