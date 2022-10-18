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
