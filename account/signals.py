from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

# Асинхронная отправка писем
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Создание профиля при создании пользователя
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )

        # Отправка приветственного письма
        context = {
            "title": "Thank you",
            "content": "We are glad you are here!",
        }
        html_content = render_to_string("emails/welcome_user.html", context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject='Welcome to our platform',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[profile.email],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        email.attach_alternative(html_content, "text/html")
        EmailThread(email).start()  # Асинхронная отправка

# Обновление пользователя при изменении профиля
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()

# Удаление пользователя при удалении профиля
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except User.DoesNotExist:
        pass
