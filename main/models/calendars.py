# import uuid as uuid_lib
# from django.db import models
# from django.utils.text import slugify
# from main.models.authenticate import Company, User
# from rest_framework import serializers

# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address1 = models.CharField(max_length=50)
#     address2 = models.CharField(max_length=50, blank=True)
#     zip_code = models.CharField(max_length=12)
#     city = models.CharField(max_length=50)
#     uuid= models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

# class Speciality(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Base(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
#     name = models.CharField(max_length=150)
#     uuid= models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

#     def __str__(self):
#         return self.name

# class Motif(models.Model): 

#     class Type(models.TextChoices):
#         NEW="NEW","NOUVEAU PATIENT",
#         FOLLOWED="FOLLOWED", "PATIENT SUIVI",
#         ALL="ALL", "TOUTES GATEGORIES"

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=150)
#     duration = models.TimeField()
#     duration_max = models.TimeField()
#     duration_min = models.TimeField()
#     reservable = models.BooleanField(default=True)
#     type = models.CharField(max_length=50, choices=Type.choices, default=Type.ALL)
#     color = models.CharField(max_length=50, blank=True, null=True)
#     uuid = models.UUIDField(db_index=True, editable=False, default= uuid_lib.uuid4)

#     def __str__(self):
#         return self.name

# class Calendar(models.Model):
#     user= models.ForeignKey(User, on_delete=models.CASCADE)
#     name= models.CharField(max_length=150)
#     created_on= models.DateTimeField(auto_now_add=True)
#     updated_on= models.DateTimeField(auto_now=True)
#     company= models.ForeignKey(Company, on_delete=models.CASCADE)
#     uuid= models.UUIDField(db_index=True, default= uuid_lib.uuid4, editable=True)
#     slug= models.SlugField(blank=True)

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#        self.slug = slugify(self.name)
#        super(Calendar, self).save(*args, **kwargs)

#     @property
#     def events(self):
#         return self.event_set
    


    


    

