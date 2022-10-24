from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import User
from accounts.services.user_service import UserService
from innoapp import tasks
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
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to see the posts of this page!")
        return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        my_page = UserService.get_current_page(self.request)
        if str(my_page.pk) != self.kwargs['page_pk']:
            raise ValidationError("You don't have a permission to create posts for this page!")
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))
        tasks.send_email(my_page.owner.email, my_page.owner.username, self.request)

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))


class PostReplyViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        page_for_post_reply = Page.objects.get(posts=self.request.data.get("reply_to"))
        if not page_for_post_reply.is_private or \
                UserService.get_user_id(self.request) in [follower.pk for follower in
                                                          page_for_post_reply.followers.filter()] or \
                UserService.get_user_id(self.request) == page_for_post_reply.owner.pk:
            serializer.save(page=page_for_post_reply)


class PostsWithMyLikesViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(liked_by=UserService.get_user_id(self.request))
        return posts


class PostLikesViewSet(viewsets.ModelViewSet):

    @action(methods=['post'], detail=False)
    def like(self, request):
        try:
            user_post = Post.objects.get(pk=request.data.get("post"))
        except ObjectDoesNotExist:
            raise ValidationError("Post does not exist!")
        if user_post.liked_by.filter(pk=UserService.get_user_id(request)).exists():
            user_post.liked_by.remove(UserService.get_user_id(request))
        else:
            user_post.liked_by.add(UserService.get_user_id(request))
        serializer = PostSerializer(user_post)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
