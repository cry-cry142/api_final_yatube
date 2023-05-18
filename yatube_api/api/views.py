from django.shortcuts import get_object_or_404
from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet,
                                     GenericViewSet)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import filters

from posts.models import Post, Group
from .serializers import (PostSerializer, GroupSerializer, CommentSerializer,
                          FollowSerializer)
from .permissions import AuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$following__username',)

    def get_queryset(self):
        user = self.request.user
        queryset = user.follower.select_related('following').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
