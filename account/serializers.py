from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import *
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validated_data

    def create(self, attrs):
        user = CustomUser.objects.create_user(**attrs)
        send_activation_code(user.email, user.activation_code)
        return user




