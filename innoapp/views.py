from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.services.user_service import UserService
from innoapp.models import Page, Post, Tag
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.filter(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_create(self, serializer):
        try:
            my_page = Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(self.request)))
            if my_page:
                raise ValidationError("Page already exists!")
        except ObjectDoesNotExist:
            serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_update(self, serializer):
        serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        my_page = UserService.get_current_page(self.request)
        print(my_page.pk)
        print(self.kwargs['page_pk'])
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to see the posts of this page!")
        return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        my_page = UserService.get_current_page(self.request)
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to create posts for this page!")
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        my_page = UserService.get_current_page(self.request)
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to see the tags of this page!")
        return Tag.objects.filter(pages=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        my_page = UserService.get_current_page(self.request)
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to create tags for this page!")
        serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))
