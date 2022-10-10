import jwt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    UserRequestsSerializer
from innoapp.models import Page
from innoapp.permissions import IsStaffOrDontSeeBlockedUser, IsStaffOrDontSeeBlockedPage, IsOwnerOrReadOnly
from accounts.generate_token import CustomTokenGenerator
from accounts.services.check_login import CheckLogin
from innotter import settings


class UserFollowersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsStaffOrDontSeeBlockedUser, IsStaffOrDontSeeBlockedPage, IsOwnerOrReadOnly)

    def get_queryset(self):
        return User.objects.filter(follows=self.kwargs['page_pk'])


class UserRequestsViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequestsSerializer
    # permission_classes = (IsStaffOrDontSeeBlockedUser, IsStaffOrDontSeeBlockedPage, IsOwnerOrReadOnly)

    def get_user(self, request):
        user_id = jwt.decode(request.headers['jwt'], settings.SECRET_KEY, algorithms=["HS256"])['user_id']
        return user_id

    def get_queryset(self):
        return User.objects.filter(requests=self.kwargs['page_pk'])

    def send_request(self, serializer):
        page_to_send_request = Page.objects.get(pk=self.kwargs['page_pk'])
        page_to_send_request.follow_requests(User.objects.filter(self.get_user(self.request)))
        # if not self.get_user(self.request) == page_to_send_request.owner:
        #     if page_to_send_request.is_private:
        #         serializer.save(requests=User.objects.filter(pk=self.get_user(self.request)))


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
