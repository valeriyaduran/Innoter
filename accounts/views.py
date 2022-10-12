from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    MyFollowersSerializer, FollowRequestsSerializer
from accounts.services.auth_service import AuthService
from accounts.services.user_service import UserService
from innoapp.serializers import PageSerializer


class UserFollowersViewSet(viewsets.ModelViewSet):

    serializer_classes = {
        'send_follow_requests': FollowRequestsSerializer,
        'my_followers': MyFollowersSerializer,
        'my_follow_requests': FollowRequestsSerializer,
        'accept_my_follow_requests': MyFollowersSerializer,
        'delete_my_follow_requests': FollowRequestsSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PageSerializer)

    @action(detail=False)
    def my_followers(self, request):
        my_page = UserService.get_current_page(request)
        serializer = self.get_serializer(my_page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def send_follow_requests(self, request):
        UserService.compare_current_and_requested_users(request)
        user_page = UserService.get_user_page_to_follow(request)
        user_page = UserService.get_user_page_to_follow(request)
        current_user = User.objects.get(pk=UserService.get_user_id(request))

        if user_page.is_private:
            user_page.follow_requests.add(current_user)
        else:
            user_page.followers.add(current_user)
        serializer = self.get_serializer(user_page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def my_follow_requests(self, request):
        my_page = UserService.get_current_page(request)
        serializer = self.get_serializer(my_page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False)
    def accept_my_follow_requests(self, request):
        my_page = UserService.get_current_page(request)
        usernames = UserService.get_usernames(request)
        if usernames:
            for username in usernames:
                my_page.followers.add(User.objects.get(username=username))
                my_page.follow_requests.remove(User.objects.get(username=username))

        serializer = self.get_serializer(my_page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False)
    def delete_my_follow_requests(self, request):
        my_page = UserService.get_current_page(request)
        usernames = UserService.get_usernames(request)
        if usernames:
            for username in usernames:
                my_page.follow_requests.remove(User.objects.get(username=username))
        serializer = self.get_serializer(my_page)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        AuthService.check_login(email, password)

        response = Response()
        response.headers = {'jwt': AuthService.generate_token(request)}
        return response

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
