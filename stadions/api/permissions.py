from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.type == 'owner'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser


class IsAdminOrOwnerStadion(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.type == 'owner'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.stadion.owner or request.user.is_superuser
