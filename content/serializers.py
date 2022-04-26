from rest_framework import serializers
from .models import Tag, MediaContent


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["body"]   


class MediaContentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MediaContent
        fields = ["title", "media_file", "tags", "media_type"]
