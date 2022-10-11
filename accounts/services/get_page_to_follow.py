from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.serializers import UserFollowersSerializer
from accounts.services.get_user_id import GetUserId
from innoapp.models import Page


class PageToFollow:
    @staticmethod
    def get_page_to_follow(request):
        serializer = UserFollowersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            page = Page.objects.get(owner=User.objects.get(pk=GetUserId.get_user_id(request)))
        except ObjectDoesNotExist:
            raise ValidationError("No page by URL provided")
        return page
