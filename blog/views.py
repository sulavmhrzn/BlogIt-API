from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter
from .models import Comment, Post
from .pagination import DefaultPageNumberPagination
from .permissions import IsCommentOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    """
    ViewSet for Post Model.
    """

    serializer_class = PostSerializer
    pagination_class = DefaultPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_permissions(self):
        """
        Allow user with staff permission to get, edit and delete post.
        else, get post only.
        """
        if self.request.user.is_staff:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_queryset(self):
        """
        Return all posts if requested user have staff permission.
        else, active posts only.
        """
        if self.request.user.is_staff:
            return (
                Post.objects.select_related("author")
                .prefetch_related("tags")
                .annotate(comments_count=Count("comments"))
            )
        return (
            Post.objects.select_related("author")
            .filter(is_active=True)
            .annotate(comments_count=Count("comments"))
        )

    def get_serializer_context(self):
        """
        Pass extra context to serializer.
        """
        context = super().get_serializer_context()
        context["author"] = self.request.user
        return context


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCommentOwnerOrReadOnly()]

    def get_serializer_context(self):
        """
        Pass extra context to serializer.
        """
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["post_pk"] = self.kwargs["post_pk"]
        return context

    def get_queryset(self):
        """
        Returns filtered comments with passed in post pk
        """
        return Comment.objects.select_related("user", "post").filter(
            post_id=self.kwargs["post_pk"]
        )
