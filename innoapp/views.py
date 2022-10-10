import jwt
from rest_framework import viewsets

from accounts.models import User
from innoapp.models import Page, Post, Tag
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer
from innotter import settings


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get_user_id(self, request):
        user_id = jwt.decode(request.headers['jwt'], settings.SECRET_KEY, algorithms=["HS256"])['user_id']
        return user_id

    def perform_create(self, serializer):
        serializer.save(owner=User.objects.get(pk=self.get_user_id(self.request)))

    def perform_update(self, serializer):
        serializer.save(owner=User.objects.get(pk=self.get_user_id(self.request)))


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_destroy(self, instance):
        instance.delete()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(pages=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))

    def perform_destroy(self, instance):
        instance.delete()
