from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from .helpers.validate_password import validate_password_strength


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "firstName", "lastName", "password", "username"]

    def create(self, validated_data):
        # Hash the password manually here
        password = validate_password_strength(validated_data["password"])
        validated_data["password"] = make_password(password)

        # Create user normally
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            firstName=validated_data["firstName"],
            lastName=validated_data["lastName"],
            password=validated_data["password"],
        )
        return user
