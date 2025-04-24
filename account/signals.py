from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import Profile, CustomUser
import threading


# Helper class for sending emails asynchronously
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


@receiver(post_save, sender=CustomUser)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            name=instance.username,
            surname="",
            location="",
            bio="",
        )

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
            to=[instance.email],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        email.attach_alternative(html_content, "text/html")
        EmailThread(email).start()

# 1104181f-00d0-4266-947a-6a500a1f798e
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.username = instance.name
        user.email = instance.user.email
        user.save()


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except CustomUser.DoesNotExist:
        pass
