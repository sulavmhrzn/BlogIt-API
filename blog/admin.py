from django.contrib import admin
from django.db.models import Count

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 25
    prepopulated_fields = {"slug": ["title"]}
    list_display = ["title", "is_active", "author", "tag_list", "count_comments"]
    list_editable = [
        "is_active",
    ]
    list_filter = ["is_active", "tags"]
    search_fields = ["title", "author__username"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("tags", "comments")
            .annotate(count_comments=Count("comments"))
        )

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    @admin.display(ordering="-count_comments", description="Comments")
    def count_comments(self, post):
        return post.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "post"]
    search_fields = ["post__title", "user__username", "text"]
