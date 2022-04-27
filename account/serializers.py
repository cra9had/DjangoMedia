from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from .models import User
from .utils import generate_activation_key
from rest_framework.exceptions import APIException
from django.core.mail import send_mail


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64, write_only=True)
    
    def validate(self, data):
        key = data["token"]
        try:
            token = Token.objects.get(key=key)
            if not token.user.is_active:
                raise ValidationError("User is not active")
        except Token.DoesNotExist:
            raise ValidationError("Incorrect token")

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, error_messages={
            "blank": "Нужно ввести почту",
        },)
    password = serializers.CharField(max_length=128, write_only=True, error_messages={
            "blank": "Нужно ввести пароль",
        },)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "Почта или пароль неверны"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Подтвердите почту'
            )

        token, _ = Token.objects.get_or_create(user_id=user.id)

        return {
            'email': user.email,
            'token': token.key
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "birthday", "sex", "fullname"]

    def create(self, validated_data):
        try:
            key = generate_activation_key(validated_data["email"])
            activation_url = self.context["activation_url"] + key
            user = User.objects.create_user(**validated_data, activation_key=key)
            user.save()
            Token.objects.create(user=user)
            send_mail('Регистрация',
                      'Перейдите по ссылке, чтобы подтвердить регистрацию: ' + activation_url,
                      'mediatags@mail.ru', [user.email], fail_silently=False)
            return validated_data
        except IntegrityError as e:
            raise APIException(e)

    def validate(self, data):
        if len(data["fullname"].split()) != 3:
            raise ValidationError({
                "fullname": "ФИО введино некорректно"
            })
        return data
