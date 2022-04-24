from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, LoginSerializer, TokenSerializer
from .models import User
from django.shortcuts import HttpResponse, Http404


def activation(request, key):
    user = get_object_or_404(User, activation_key=key)
    if not user.is_active:
        user.is_active = True
        user.save()
        return HttpResponse("Email activated")
    return Http404()


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={"activation_url": request.build_absolute_uri("/account/activate/")})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


