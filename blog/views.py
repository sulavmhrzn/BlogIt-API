from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter
from .models import Post
from .pagination import DefaultPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


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
            return Post.objects.select_related("author").prefetch_related("tags").all()
        return Post.objects.select_related("author").filter(is_active=True)

    def get_serializer_context(self):
        """
        Pass extra context to serializer.
        """
        context = super().get_serializer_context()
        context["author"] = self.request.user
        return context
