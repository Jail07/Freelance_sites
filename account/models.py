from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        if not username:
            raise ValueError('The Username field must be set.')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email должен быть уникальным
    objects = CustomUserManager()  # Связываем менеджер с моделью

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=200, blank=False, null=False)
    surname = models.CharField(max_length=200, blank=False, null=False)
    location = models.CharField(max_length=200, blank=False, null=False)
    bio = models.TextField(blank=True, null=False)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/profiles/",
        default="images/profiles/user-default.png",
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user or "Unnamed User")

    class Meta:
        ordering = ["-created"]

    @property
    def imageURL(self):
        if self.profile_image and hasattr(self.profile_image, "url"):
            return self.profile_image.url
        return "images/profiles/user-default.png"


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="skills")
    name = models.CharField(max_length=200, blank=False, null=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)  # Поле для отслеживания прочтения
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"
