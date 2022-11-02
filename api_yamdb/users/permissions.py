from rest_framework.permissions import BasePermission

from .models import ADMIN, MODERATOR


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.role == ADMIN
                or user.is_superuser)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == MODERATOR
