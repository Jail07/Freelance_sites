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


# Signal to create a Profile when a new CustomUser is created
@receiver(post_save, sender=CustomUser)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            name=instance.username,  # Initial name matches username
            surname="",
            location="",
            bio="",
        )

        # Send welcome email
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


# Signal to update the CustomUser when the Profile is updated
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.username = instance.name  # Update username based on profile name
        user.email = instance.user.email  # No changes to email here
        user.save()


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except CustomUser.DoesNotExist:
        pass
