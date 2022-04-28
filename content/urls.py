from django.urls import path
from .views import GetTagsAPIView, GetMediaContentAPIView, ChoiceMediaAPIView


urlpatterns = [
    path('tags', GetTagsAPIView.as_view()),
    path('content', GetMediaContentAPIView.as_view()),
    path('choose', ChoiceMediaAPIView.as_view())
]
