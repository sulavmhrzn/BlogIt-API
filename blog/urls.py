from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register("post", views.PostViewSet, basename="posts")

comments_router = NestedDefaultRouter(router, "post", lookup="post")
comments_router.register("comments", views.CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comments_router.urls)),
]
