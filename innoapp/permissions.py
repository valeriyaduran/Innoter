import datetime
from dateutil import parser

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import permissions

from accounts.models import User
from accounts.services.user_service import UserService
from innoapp.models import Page


class IsAdminModeratorOrForbidden(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            current_user = User.objects.get(pk=UserService.get_user_id(request))
        except ObjectDoesNotExist:
            raise ValidationError("User not found")
        if current_user.is_staff:
            return True


class IsStaffOrDontSeeBlockedData(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST' and request.path == '/api/v1/pages/':
            return True
        else:
            page = UserService.get_current_page(request)
            # print(page)
            if User.objects.get(pk=UserService.get_user_id(request)).is_staff:
                # print("is staff")
                return True
            elif page.unblock_date:
                if page.unblock_date.timestamp() < datetime.datetime.utcnow().timestamp():
                    # print("unblock date exists")
                    return True
            else:
                # print("no unblock date")
                return True


