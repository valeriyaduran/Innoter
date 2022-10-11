from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from accounts.generate_token import CustomTokenGenerator
from accounts.services.check_login import CheckLogin
from accounts.services.get_page_to_follow import PageToFollow


class UserFollowersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['get', 'put'], detail=False)
    def followers(self, request):
        if self.request.method == 'GET':
            return PageToFollow.get_page_to_follow(request).followers

        if self.request.method == 'PUT':
            if PageToFollow.get_page_to_follow(request).is_private:
                self.follow_requests(self, request)
            else:
                PageToFollow.get_page_to_follow(request).followers.append(
                    User.objects.get(
                        username=PageToFollow.get_page_to_follow(request).serializer.validated_data.get('username')))
        return Response(PageToFollow.get_page_to_follow(request).serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['get', 'put'], detail=False)
    def follow_requests(self, request):
        if self.request.method == 'GET':
            return PageToFollow.get_page_to_follow(request).follow_requests
        if self.request.method == 'PUT':
            if not PageToFollow.get_page_to_follow(request).is_private:
                self.followers(self, request)
            else:
                PageToFollow.get_page_to_follow(request).follow_requests.append(
                    User.objects.get(
                        username=PageToFollow.get_page_to_follow(request).serializer.validated_data.get('username')))
        return Response(PageToFollow.get_page_to_follow(request).serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['put', 'delete'], detail=False)
    def accept_follow_requests(self, request):
        if self.request.method == 'PUT':
            for username in self.request.data.get('username'):
                PageToFollow.get_page_to_follow(request).followers.append(
                    User.objects.get(username=username))
        if self.request.method == 'DELETE':
            for username in self.request.data:
                PageToFollow.get_page_to_follow(request).followers.remove(
                    User.objects.get(username=username))


class AuthViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        CheckLogin.check_login(email, password)

        response = Response()
        response.headers = {'jwt': CustomTokenGenerator.generate_token(request)}
        return response

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
