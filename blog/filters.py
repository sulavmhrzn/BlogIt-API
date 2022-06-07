import django_filters
from django import forms
from django.db import models
from django_filters.rest_framework import FilterSet

from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = ["is_active", "tags__name"]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
            models.BooleanField: {
                "filter_class": django_filters.BooleanFilter,
                "extra": lambda f: {
                    "widget": forms.CheckboxInput,
                },
            },
        }
