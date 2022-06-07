from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 25
    prepopulated_fields = {"slug": ["title"]}
    list_display = ["title", "is_active", "author", "tag_list"]
    list_editable = [
        "is_active",
    ]
    list_filter = ["is_active", "tags"]
    search_fields = ["title", "author__username"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
