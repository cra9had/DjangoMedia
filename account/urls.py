from django.urls import path, re_path
from .views import RegistrationAPIView, activation, LoginAPIView


urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    re_path(r'^activate/(?P<key>.+)$', activation),
    path('login', LoginAPIView.as_view())
]
