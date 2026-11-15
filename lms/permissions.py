from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """Разрешение для модераторов (проверка группы)."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()

class IsOwner(BasePermission):
    """Разрешение для владельцев объектов."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
