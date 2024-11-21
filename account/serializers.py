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
        print(attrs, "djshakjshksjadh")
        user = CustomUser.objects.create_user(**attrs)
        send_activation_code(user.email, user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request '),
                                email=email, password=password)
            if not user:
                message = 'No authenticate!!!'
                raise serializers.ValidationError(message, code='authentication')
        else:
            message = 'Must include "email" and "password'
            raise serializers.ValidationError(message, code='authentication')

        attrs['user'] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = {'name', 'surname', 'birthdate', 'phone', 'bio', 'location', 'skills', 'photo'}
