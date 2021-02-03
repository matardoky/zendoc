from rest_framework import serializers
from models.users import User, Company
from rest_auth.registration.serializers import RegisterSerializer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__" 


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = "__all__"

class Register(serializers.Serializer):


    