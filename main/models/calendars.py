import uuid as uuid_lib
from django.db import models
from .authenticate import Company, User
from rest_framework import serializers

class Address(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    uuid= models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

class Speciality(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Base(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    uuid= models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

    def __str__(self):
        return self.name

class Motif(models.Model): 

    class Type(models.TextChoices):
        NEW="NEW","NOUVEAU PATIENT",
        FOLLOWED="FOLLOWED", "PATIENT SUIVI",
        ALL="ALL", "TOUTES GATEGORIES"

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    duration= models.TimeField()
    duration_max= models.TimeField()
    duration_min= models.TimeField()
    reservable= models.BooleanField(default=True)
    type= models.CharField(max_length=50, choices=Type.choices, default=Type.ALL)
    color= models.CharField(max_length=50, blank=True, null=True)
    uuid= models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)
    company= models.ForeignKey(Company, on_delete=models.CASCADE)
    uuid= models.UUIDField(db_index=True, default= uuid_lib.uuid4, editable=True)

    def __str__(self):
        return self.name
    

class SpecialtySerializer(serializers.ModelSerializer):
    pass

class AddressSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Address
        fields= ('__all__')

class BaseSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Base
        fields= ('__all__')

class MotifSerializer(serializers.ModelSerializer):
    class Meta:
        model= Motif
        fields= ('__all__')

class CalendarSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Calendar
        fields= ('__all__')


    


    

