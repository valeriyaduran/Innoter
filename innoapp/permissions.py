import datetime


from rest_framework import permissions
from rest_framework.exceptions import NotFound

from innoapp.models import Page


class IsStaffOrDontSeeBlockedPage(permissions.BasePermission):
    def get_unblock_date(self):
        current_page_unblock_date = Page.objects.get(page=self.kwargs['page_pk']).unblock_date
        return current_page_unblock_date

    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff:
            if self.get_unblock_date() > datetime.datetime.utcnow():
                raise NotFound("The page is not found")


class IsStaffOrDontSeeBlockedUser(permissions.BasePermission):
    def get_user(self):
        current_user = Page.objects.get(page=self.kwargs['page_pk']).owner
        return current_user

    def has_object_permission(self, request, view, obj):
        if self.get_user().is_blocked:
            if not request.user.is_staff:
                raise NotFound("The page is not found")


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, ):
        if Page.objects.get(page=self.kwargs['page_pk']).owner == request.user or request.user.is_staff:
            return True
        return False

