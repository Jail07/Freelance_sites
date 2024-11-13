from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import *


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully registered", status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(email=email,
                                         activation_code=activation_code).first()
        print(user)
        print(email)
        if not user:
            return Response('This user does not exits', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Your account successfully activated', status=status.HTTP_200_OK)


# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer
#
#
# class LogoutVew(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def post(self, request):
#         user = request.user
#         Token.objects.filter(user=user)
#         return Response('Successfully logged out', status=status.HTTP_200_OK)
