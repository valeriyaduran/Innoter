from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from accounts.exceptions.user_exceptions import CurrentUserNotFound
from accounts.models import User
from accounts.services.user_service import UserService


class IsAdminOrForbidden(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            current_user = User.objects.get(pk=UserService.get_user_id(request))
        except ObjectDoesNotExist:
            raise CurrentUserNotFound()
        if current_user.is_superuser:
            return True
