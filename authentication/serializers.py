import re

from django.contrib.auth import authenticate
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from authentication.backends import JWTAuthentication
from authentication.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta: 
        model = User
        fields = ["email", "username", "password", "token"]

    def validate(self, data):

        password = data.get("password", None)

        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z]).*", password):
            raise serializers.ValidationError(
                "A password must contains atleast one small letter and one capital letter"
            )

        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                " A password must contain atleast one number"
            )

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError(
                "An email address is required to log in."
            )
        if password is None:
            raise serializers.ValidationError(
                "A password is required to log."
            )
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                " A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated."
            )

        return {
            "email": email,
            "username": user.username,
            "token":user.token
        }

      