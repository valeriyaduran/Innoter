import datetime


from rest_framework import permissions
from rest_framework.exceptions import NotFound


class IsStaffOrDontSeeBlockedPage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff:
            if obj.unblock_date > datetime.datetime.utcnow():
                raise NotFound("The page is not found")


class IsStaffOrDontSeeBlockedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_blocked:
            if not request.user.is_staff:
                raise NotFound("The page is not found")


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, ):
        if obj.owner == request.user or request.user.is_staff:
            return True
        return False

