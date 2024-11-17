from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthorPermission
from rest_framework.viewsets import ModelViewSet

from main.models import *
from main.serializers import *


class PermissionMixin:
    def get_permission(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PostViewSet(PermissionMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


# class StarView(PermissionMixin, APIView):
#
#     def post(self, request):
#         data = request.data
#         serializer = StarSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response("add star", status=status.HTTP_200_OK)
#







