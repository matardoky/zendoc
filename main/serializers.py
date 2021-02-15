from rest_framework import serializers
from main.models.authenticate import User, Company
from main.models.rules import Rule

from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "slug", "uuid"]

    def validate_name(self, value):
        if Company.objects.filter(name__iexact=value):
            raise serializers.ValidationError("company existe déjà")
        return value
        
class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'

class CustomRegisterSerializer(RegisterSerializer):
    is_admin = serializers.BooleanField()
    company = CompanySerializer()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'is_admin': self.validated_data.get('is_admin', ''),
            'company': self.validated_data.get('company', ''),
        }
 
    def save(self,request): 
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        company_data = self.cleaned_data.pop('company')
        company = Company.objects.create(**company_data)
        user.company = company
        user.is_admin = self.cleaned_data.get("is_admin")
        user.save()
        adapter.save_user(request, user, self)
        return user
    
        
class RuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rule
        fields = ["frequency", "_week_day"]




    