from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Comment, Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Serializer for Post Model.
    -> tags (https://django-taggit.readthedocs.io/en/latest/serializers.html)
    -> Represent author with its string representation
    """

    tags = TagListSerializerField()
    author = serializers.StringRelatedField()
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "tags",
            "is_active",
            "comments_count",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
        ]

    def create(self, validated_data):
        """
        Create Post object with passed in user as author, and validated datas.
        """
        return Post.objects.create(author=self.context["author"], **validated_data)


class PostListSerializer(PostSerializer):
    """
    Post serializer that excludes description.
    """

    class Meta(PostSerializer.Meta):
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "is_active",
            "comments_count",
            "author",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment Model
    """

    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "user",
        ]

    def create(self, validated_data):
        """
        Create comment object with passed in authenticated user.
        """
        return Comment.objects.create(
            user=self.context["user"], post_id=self.context["post_pk"], **validated_data
        )
