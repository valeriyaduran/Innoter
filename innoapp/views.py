from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.services.user_service import UserService
from innoapp.models import Page, Post, Tag
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        try:
            Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(self.request)))
        except ObjectDoesNotExist:
            serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_update(self, serializer):
        serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        try:
            page = Page.objects.get(pk=self.kwargs['page_pk'])
        except ObjectDoesNotExist:
            raise ValidationError("No page by URL provided")
        if page:
            serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(pages=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        try:
            page = Page.objects.get(pk=self.kwargs['page_pk'])
        except ObjectDoesNotExist:
            raise ValidationError("No page by URL provided")
        if page:
            serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))
