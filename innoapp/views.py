from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import User
from accounts.services.user_service import UserService
from innoapp.models import Page, Post, Tag
from innoapp.permissions import IsAdminModeratorOrForbidden, IsAdminModeratorOrDontSeeBlockedContent
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Page.objects.all()
        else:
            return Page.objects.filter(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_create(self, serializer):
        try:
            my_page = Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(self.request)))
            if my_page:
                raise ValidationError("Page already exists!")
        except ObjectDoesNotExist:
            serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_update(self, serializer):
        serializer.save(owner=Page.objects.get(pk=int(self.kwargs['pk'])).owner)


class BlockPageByStaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrForbidden]

    @action(methods=['put'], detail=False)
    def block_page(self, request):
        page_to_block = UserService.set_unblock_date(request)
        serializer = PageSerializer(page_to_block)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Post.objects.filter(page=self.kwargs['page_pk'])
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to see the posts of this page!")
            return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        if UserService.is_admin_or_moderator(self.request):
            serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to create posts for this page!")
            serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_destroy(self, instance):
        if UserService.is_admin_or_moderator(self.request) or str(UserService.get_current_page(
                self.request).pk) == self.kwargs['page_pk']:
            instance.delete()


class PostReplyViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def perform_create(self, serializer):
        page_for_post_reply = Page.objects.get(posts=self.request.data.get("reply_to"))
        if not page_for_post_reply.is_private or \
                UserService.get_user_id(self.request) in [follower.pk for follower in
                                                          page_for_post_reply.followers.filter()] or \
                UserService.get_user_id(self.request) == page_for_post_reply.owner.pk:
            serializer.save(page=page_for_post_reply)


class PostsWithMyLikesViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        posts = Post.objects.filter(liked_by=UserService.get_user_id(self.request))
        return posts


class PostLikesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

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
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Tag.objects.filter(pages=self.kwargs['page_pk'])
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to see the tags of this page!")
            return Tag.objects.filter(pages=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        if UserService.is_admin_or_moderator(self.request):
            serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to create tags for this page!")
            serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))
