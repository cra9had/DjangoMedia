from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    body = models.CharField("Тег", max_length=128, unique=True)

    def __str__(self):
        return self.body


class MediaContent(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 1, "Изображение"
        VIDEO = 2, "Видео"
        AUDIO = 3, "Аудио"

    title = models.CharField("Название", max_length=128)
    media_file = models.FileField("Медиа файл", upload_to="content/%Y/%m/%d")
    media_type = models.CharField(verbose_name="Тип", max_length=20, choices=MediaType.choices, default=MediaType.IMAGE)
    tags = models.ManyToManyField(Tag, verbose_name="Теги")

    def __str__(self):
        return self.title


class ChosenMediaContent(models.Model):
    media_content = models.ForeignKey(MediaContent, on_delete=models.CASCADE, verbose_name="Выбранный медиа-контент")
    tags = models.ManyToManyField(Tag, verbose_name="Выбранные теги")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}. {self.user.email} | {self.media_content.title}"
