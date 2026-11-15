from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    """Разрешение: пользователь может редактировать только свой профиль."""
    def has_object_permission(self, request, view, obj):
        return obj == request.user
