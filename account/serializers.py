import os

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.files import File
from rest_framework.exceptions import ValidationError

from .models import Profile, Skill, Message, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True, source='skill_set')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'location', 'bio', 'profile_image', 'skills', 'created']
        read_only_fields = ['id', 'profile_image']

    def create(self, validated_data):
        request_user = self.context['request'].user
        if not request_user or not request_user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a profile.")

        profile = Profile.objects.create(user=request_user, **validated_data)

        profile_image_path = self.context['request'].data.get('profile_image', None)
        if profile_image_path:
            if os.path.exists(profile_image_path):  # Проверяем существование файла
                with open(profile_image_path, "rb") as image_file:
                    profile.profile_image.save(os.path.basename(profile_image_path), File(image_file))
            else:
                raise ValidationError({"profile_image": "Файл по указанному пути не найден."})

        profile.save()
        return profile

    def update(self, instance, validated_data):
        profile_image_path = self.context['request'].data.get('profile_image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_image_path:
            if os.path.exists(profile_image_path):
                with open(profile_image_path, "rb") as image_file:
                    instance.profile_image.save(os.path.basename(profile_image_path), File(image_file))
            else:
                raise ValidationError({"profile_image": "Файл по указанному пути не найден."})

        instance.save()
        return instance



class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    recipient = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'is_read', 'created']
        read_only_fields = ['id', 'sender', 'recipient', 'is_read', 'created']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=password,
            email=validated_data['email'],
            is_active=True
        )
        return user

