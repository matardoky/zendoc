import uuid as uuid_lib
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, 
    PermissionsMixin
)
from django.utils.text import slugify


class CompanyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Company(models.Model):
    objects = CompanyManager()
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(
            "The given email must be set"
            )
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

    def create_user(self, email, company, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
               "Superuser must have is_staff=True"
            )
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )
        return self._create_user(email, password, **extra_fields)

        
class User(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        ADMIN= "ADMIN", "ADMIN"
        PRATICIEN="PRATICIEN", "PRATICIEN"
        SECRETAIRE="SECRETAIRE", "SECREATIRE"
        AGENT_ADMIN="AGENT_ADMIN","AGENT ADMINISTRATIVE"
        PERSON_SOIN="PERSON_SOIN", "PERSONNELS DE SOIN"

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=225, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)     
    type = models.CharField(max_length=50, choices=Types.choices, default = Types.AGENT_ADMIN)
    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE, 
        blank=True, 
        null=True
    )
    username = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()



