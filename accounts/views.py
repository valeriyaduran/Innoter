from rest_framework import viewsets

from accounts.models import User
from accounts.serializers import UserSerializer
from innoapp.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(follows=self.kwargs['page_pk'])


class UserRequestsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(requests=self.kwargs['page_pk'])