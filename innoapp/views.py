from rest_framework import viewsets

from innoapp.models import Page, Post
from innoapp.serializers import PageSerializer, PostSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    # @action(methods=['get'], detail=True, serializer_class=PostSerializer)
    # def posts(self, request, pk=None):
    #     posts = Post.objects.filter(page=pk).values()
    #     return Response(posts)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(page=self.kwargs['page_pk'])
