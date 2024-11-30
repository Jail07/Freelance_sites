from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

# SkillSerializer для управления навыками
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # Используем вложенный сериализатор User
    skills = SkillSerializer(many=True, read_only=True, source='skill_set')  # Вложенные навыки


    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'email', 'username', 'location', 'bio', 'profile_image', 'skills', 'created']  # Или укажите поля явно, если нужно
        read_only_fields = ['id']

    def create(self, validated_data):
        # Если нужно создать профиль
        user_data = validated_data.pop('user', None)  # Извлекаем данные пользователя (если передаются)
        if user_data:
            user = User.objects.create(**user_data)
            profile = Profile.objects.create(user=user, **validated_data)
        else:
            profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        # Обновляем профиль и вложенные данные пользователя
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



# MessageSerializer для работы с сообщениями
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
