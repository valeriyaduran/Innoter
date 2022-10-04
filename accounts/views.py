from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.generate_token import CustomTokenGenerator
from accounts.services.check_login import CheckLogin


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(follows=self.kwargs['page_pk'])


class UserRequestsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(requests=self.kwargs['page_pk'])


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer


class LoginViewSet(viewsets.ModelViewSet):
    def post(self, request):
        CheckLogin.check_login(request)
        response = Response()
        response.headers = {'jwt': CustomTokenGenerator.generate_token(request)}
        return response


class LogoutViewSet(viewsets.ModelViewSet):
    def post(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
