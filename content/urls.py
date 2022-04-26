from django.urls import path
from .views import GetTagsAPIView, GetMediaContentAPIView


urlpatterns = [
    path('tags', GetTagsAPIView.as_view()),
    path('content', GetMediaContentAPIView.as_view())
]
