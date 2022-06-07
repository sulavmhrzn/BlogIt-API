from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Serializer for Post Model.
    -> tags (https://django-taggit.readthedocs.io/en/latest/serializers.html)
    -> Represent author with its string representation
    """

    tags = TagListSerializerField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "tags",
            "is_active",
            "author",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Create Post object with passed in user as author, and validated datas.
        """
        return Post.objects.create(author=self.context["author"], **validated_data)
