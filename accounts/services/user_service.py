import datetime

import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.http import HttpResponseForbidden

from accounts.models import User
from innoapp.models import Page
from innotter import settings


class UserService:
    @staticmethod
    def get_user_id(request):
        try:
            user_id = jwt.decode(request.headers['jwt'], settings.SECRET_KEY, algorithms=["HS256"])['user_id']
        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden("Invalid signature or signature has expired")
        return user_id

    @staticmethod
    def get_usernames(request):
        try:
            usernames = request.data.get('username')
        except ObjectDoesNotExist:
            raise ValidationError("No username provided")
        return usernames

    @staticmethod
    def compare_current_and_requested_users(request):
        current_user = UserService.get_user_id(request)
        try:
            requested_user = User.objects.get(
                username=request.data.get('username')
            ).pk
        except ObjectDoesNotExist:
            raise ValidationError("No user by username provided")
        if current_user == requested_user:
            raise ValidationError("You are not able to follow or accept yourself as a follower of your own page ")

    @staticmethod
    def get_user_page(request):
        try:
            page = Page.objects.get(owner=User.objects.get(username=request.data.get("username")))
        except ObjectDoesNotExist:
            raise ValidationError("No page by URL provided")
        return page

    @staticmethod
    def get_current_page(request):
        try:
            page = Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(request)))
        except ObjectDoesNotExist:
            raise ValidationError("No page by URL provided")
        return page

    @staticmethod
    def set_unblock_date(request):
        page_to_block = UserService.get_user_page(request)
        unblock_datetime = request.data.get('unblock_date')
        if datetime.datetime.now().date() > unblock_datetime.date():
            page_to_block.unblock_date = unblock_datetime
        else:
            raise ValidationError("Unblock date must be later than today")
        return page_to_block

