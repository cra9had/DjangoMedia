from rest_framework import serializers
from .models import Tag, MediaContent, ChosenMediaContent


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["pk", "body"]
        read_only_fields = ["pk"]


class MediaContentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MediaContent
        fields = ["pk", "title", "media_file", "tags", "media_type"]
        read_only_fields = ["pk"]


class GetChosenMediaSerializer(serializers.Serializer):
    tags = TagSerializer(many=True, read_only=True)
    media_content = MediaContentSerializer(read_only=True)


class ChoiceMediaContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChosenMediaContent
        fields = ['media_content', 'tags']

    def create(self, validated_data):
        validated_data['user'] = self.context.get("user")
        obj = ChosenMediaContent.objects.create(user=validated_data["user"],
                                                media_content=validated_data["media_content"])
        obj.save()
        obj.tags.set(validated_data["tags"])
        return obj

