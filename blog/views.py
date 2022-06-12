from django.core.mail import BadHeaderError, send_mail
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter
from .models import Comment, Post
from .pagination import DefaultPageNumberPagination
from .permissions import IsCommentOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import CommentSerializer, PostListSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    """
    ViewSet for Post Model.
    """

    serializer_class = PostSerializer
    pagination_class = DefaultPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def create(self, request, *args, **kwargs):
        """
        Overwrite creation to send email after successfull post creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self._send_mail(serializer.data["title"], request.user.email)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def _send_mail(self, title, email):
        """
        Send email to the user that created the post.
        """
        try:
            send_mail(
                subject=f"Post created: {title}",
                message="Post created",
                from_email="sulav@admin.com",
                recipient_list=[email],
            )
        except BadHeaderError:
            return Response("Invalid header found")

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
                .order_by("-created_at")
            )
        return (
            Post.objects.select_related("author")
            .filter(is_active=True)
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        """
        Pass extra context to serializer.
        """
        context = super().get_serializer_context()
        context["author"] = self.request.user
        return context

    def get_serializer_class(self):
        """
        Returns PostListSerializer wihout description in list
        PostSerializer with description in retriieve
        """
        if self.request.method == "GET" and not self.kwargs.get("pk", ""):
            return PostListSerializer
        return PostSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Allow object user and user with staff permission to edit and delete comments
        else, get only
        """
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
