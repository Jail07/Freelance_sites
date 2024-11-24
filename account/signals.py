from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags


# @receiver(post_save, sender=Profile)

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        context = {
            "title": "Thank you",
            "content": "We are glad you are here!"
        }
        html_content = render_to_string("emails/welcome_user.html", context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject='welcome',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[profile.email],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
