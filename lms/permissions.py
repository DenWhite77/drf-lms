from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Разрешение: только для пользователей из группы 'Модераторы'."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):
    """Разрешение: только для владельца объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerAndNotModerator(BasePermission):
    """Разрешение: владелец объекта, но не модератор."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.groups.filter(name='Модераторы').exists():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModeratorOrOwner(BasePermission):
    """Разрешение: модератор ИЛИ владелец объекта."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Если пользователь модератор — разрешаем
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        # Иначе проверяем, что он владелец
        return obj.owner == request.user
