from django.contrib import admin
from .models import Tag, MediaContent


class ContentInline(admin.TabularInline):
    model = MediaContent.tags.through


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    inlines = [
        ContentInline,
    ]


@admin.register(MediaContent)
class ContentModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
