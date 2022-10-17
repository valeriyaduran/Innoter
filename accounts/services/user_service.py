import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

from accounts.exceptions.user_exceptions import UsernameNotFound, UnableToFollow
from accounts.models import User
from innoapp.exceptions.page_exceptions import CurrentUserPageNotFound, PageToFollowNotFound
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
            raise UsernameNotFound()
        return usernames

    @staticmethod
    def compare_current_and_requested_users(request):
        current_user = UserService.get_user_id(request)
        try:
            requested_user = User.objects.get(
                username=request.data.get('username')
            ).pk
        except ObjectDoesNotExist:
            raise UsernameNotFound()
        if current_user == requested_user:
            raise UnableToFollow()

    @staticmethod
    def get_user_page_to_follow(request):
        try:
            page = Page.objects.get(owner=User.objects.get(username=request.data.get("username")))
        except ObjectDoesNotExist:
            raise PageToFollowNotFound()
        return page

    @staticmethod
    def get_current_page(request):
        try:
            page = Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(request)))
        except ObjectDoesNotExist:
            raise CurrentUserPageNotFound()
        return page
