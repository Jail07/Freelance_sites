from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import ProfilePagination, search_profiles

from .models import Profile, Skill, Message
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    SkillSerializer,
    MessageSerializer,
    RegistrationSerializer,
)

# Получение JWT токена
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Регистрация пользователя
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Профили пользователей
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProfilePagination

    def get_queryset(self):
        """
        Возвращает профили текущего пользователя. Если параметр `search` передан,
        выполняется поиск по имени или навыкам.
        """
        search_query = self.request.query_params.get('search', None)
        if getattr(self, 'swagger_fake_view', False) or isinstance(self.request.user, AnonymousUser):
            return Profile.objects.none()
        if search_query:
            return search_profiles(search_query).filter(user=self.request.user)
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Создаёт профиль, привязывая его к текущему пользователю.
        """
        # Проверка на существующий профиль (если должен быть уникальным)
        if Profile.objects.filter(user=self.request.user).exists():
            raise ValidationError("Профиль для данного пользователя уже существует.")
        serializer.save(user=self.request.user)

# Навыки
class SkillViewSet(ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or isinstance(self.request.user, AnonymousUser):
            return Profile.objects.none()
        return Skill.objects.filter(owner=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


# Сообщения
class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or isinstance(self.request.user, AnonymousUser):
            return Profile.objects.none()
        return Message.objects.filter(recipient=self.request.user.profile)

    def perform_create(self, serializer):
        sender = self.request.user.profile if self.request.user.is_authenticated else None
        serializer.save(sender=sender)

# API маршруты
@api_view(['GET'])
def get_routes(request):
    routes = [
        {'POST': '/api/account/login/'},
        {'POST': '/api/account/register/'},
        {'GET': '/api/profile/'},
        {'GET': '/api/skills/'},
        {'GET': '/api/messages/'},
    ]
    return Response(routes)
