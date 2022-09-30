from rest_framework import viewsets


from innoapp.models import Page, Post, Tag
from innoapp.permissions import IsOwnerOrReadOnly
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    # @action(methods=['get'], detail=True, serializer_class=PostSerializer)
    # def posts(self, request, pk=None):
    #     posts = Post.objects.filter(page=pk).values()
    #     return Response(posts)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(page=self.kwargs['page_pk'])


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Tag.objects.filter(pages=self.kwargs['page_pk'])
