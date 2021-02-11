from django.db import models

from .authenticate import Company, User
from .rules import Rule

class Address(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE
    )

class Speciality(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Base(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Motif(models.Model): 

    class Type(models.TextChoices):
        NEW="NEW","NOUVEAU PATIENT",
        FOLLOWED="FOLLOWED", "PATIENT SUIVI",
        ALL="ALL", "TOUTES GATEGORIES"

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    duration = models.TimeField()
    duration_max = models.TimeField()
    duration_min = models.TimeField()
    reservable = models.BooleanField(default=True)
    type = models.CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.ALL
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Planning(models.Model):
    calendar = models.ForeignKey(
        Calendar, 
        on_delete=models.CASCADE
    )
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    creator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="creator"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    rule = models.ForeignKey(
        Rule, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    motif = models.ForeignKey(
        Motif,
        on_delete=models.CASCADE
    )

class Occurrence(models.Model):
    pass

