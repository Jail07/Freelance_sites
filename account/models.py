from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from main import *


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    freelancer = models.IntegerField(default=0)
    employer = models.IntegerField(default=0)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email not provided')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=25, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def create_activation_code(self):
        code = get_random_string(length=25, allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890!@#$%&')
        self.activation_code = code

    def __str__(self):
        return self.email


class Profile(models.Model):
    id_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.TextField()
    skills = models.TextField()
    rating = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return self.bio
