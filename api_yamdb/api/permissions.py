from rest_framework import permissions
from reviews.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.role == ADMIN
                or user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or request.user.is_staff)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == MODERATOR
