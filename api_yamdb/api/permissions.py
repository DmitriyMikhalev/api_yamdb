from rest_framework import permissions
from reviews.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.role == ADMIN
                or user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (request.method == 'GET' or (user.is_authenticated
                and user.role == ADMIN or user.is_superuser))

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method == 'GET' or (user.is_authenticated
                and user.role == ADMIN or user.is_superuser))


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == MODERATOR
