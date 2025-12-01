from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value


class LoginValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
