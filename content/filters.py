from django_filters import rest_framework as filters
from .models import Tag


class TagFilter(filters.FilterSet):
    body = filters.CharFilter(field_name="body", lookup_expr="startswith")

    class Meta:
        model = Tag
        fields = ["body"]
