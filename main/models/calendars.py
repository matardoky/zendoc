from django.db import models


from .authenticate import Company, User

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

class Motif(models.Models): 
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Event(models.Model):
    calendar = models.ForeignKey(calendar, on_delete=models.CASCADE)