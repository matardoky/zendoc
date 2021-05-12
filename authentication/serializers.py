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