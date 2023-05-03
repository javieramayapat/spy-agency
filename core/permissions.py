from rest_framework.permissions import BasePermission


class IsManagerOrBigBoss(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_manager or user.id == 1)


class IsBigBoss(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.id == 1