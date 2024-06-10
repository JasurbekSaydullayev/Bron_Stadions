from rest_framework import permissions


class IsAdminOrStadionOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.type == "owner"

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.stadion.owner

