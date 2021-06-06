from rest_framework import permissions


# TODO ПЕРМИШШЕНЫ ПОКА НЕ ТРОГАТЬ


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdminOrDeny(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == 'admin' or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin' or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin'
                    or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS

    # TODO ВРЕМЕННО
    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_authenticated:
    #         return request.user.role == 'admin'
    #     return request.method in permissions.SAFE_METHODS


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        result = request.method in permissions.SAFE_METHODS
        return result

    def has_object_permission(self, request, view, obj):
        return ((obj.author == request.user)
                or (request.method in permissions.SAFE_METHODS))


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'moderator'
                    or request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'moderator'
                    or request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS


class IsAdminOrModeratorAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role in {'admin', 'moderator'}
                    or request.user.is_superuser or obj.author == request.user)
        return request.method in permissions.SAFE_METHODS
