from rest_framework import serializers
from main.models.users import User, Company
from rest_auth.registration.serializers import RegisterSerializer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "slug", "uuid"]


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        





    