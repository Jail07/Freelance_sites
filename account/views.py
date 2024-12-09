from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate

from .utils import Pagination, search_profiles, paginateProfile

from .models import Profile, Skill, Message, CustomUser
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    SkillSerializer,
    MessageSerializer,
    RegistrationSerializer,
)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
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


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={201: RegistrationSerializer},
    )
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

class ProfileDetailView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, pk):

        project = get_object_or_404(Profile, id=pk)
        serializer = ProfileSerializer(project, many=False)
        return Response(serializer.data)

class MyProfileDetailView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={201: ProfileSerializer},
    )
    def post(self, request):
        if Profile.objects.filter(user=request.user).exists():
            raise ValidationError("Профиль для данного пользователя уже существует.")

        serializer = ProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer},
    )
    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer},
    )
    def patch(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise ValidationError("Вы не можете редактировать профиль другого пользователя.")

        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
            profile.delete()
            return Response({"detail": "Profile deleted successfully!"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"detail": "Something went to wrong"}, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        profiles, search_query = search_profiles(request)
        paginated_data = paginateProfile(request, profiles)
        print(paginated_data)

        serializer = ProfileSerializer(paginated_data['profiles'], many=True)
        return Response({
            "profiles": serializer.data,
            "current_page": request.GET.get('page', 1),
            "search_query": search_query,
            "total_profiles": len(profiles),
        })


class SkillView(APIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request):
        return Skill.objects.filter(owner=self.request.user.profile)

    @swagger_auto_schema(
        request_body=SkillSerializer,
        responses={201: SkillSerializer},
    )
    def post(self, serializer):
        serializer.save(owner=self.request.user.profile)


class MessageView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.profile
        messages = Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={201: MessageSerializer},
    )
    def post(self, request):
        sender = request.user.profile
        recipient_username = request.data.get('recipient')
        print(recipient_username)


        if not recipient_username:
            raise ValidationError({'recipient': 'Recipient username is required.'})

        print(recipient_username['username'])
        try:
            recipient_user = CustomUser.objects.get(email=recipient_username['email'])
            recipient = recipient_user.profile
        except CustomUser.DoesNotExist:
            raise ValidationError({'recipient': 'Recipient not found.'})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=sender, recipient=recipient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDeatailView(APIView):
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={201: MessageSerializer},
    )
    def put(self, request, pk):
        message = get_object_or_404(Message, pk=pk, sender=request.user.profile)

        if message.is_read:
            raise PermissionDenied("Cannot edit a message that has already been read by the recipient.")

        serializer = self.serializer_class(message, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={201: MessageSerializer},
    )
    def patch(self, request, pk):
        message = get_object_or_404(Message, pk=pk, sender=request.user.profile)

        if message.is_read:
            raise PermissionDenied("Cannot edit a message that has already been read by the recipient.")

        serializer = self.serializer_class(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = get_object_or_404(Message, pk=pk, sender=request.user.profile)

        if message.is_read:
            raise PermissionDenied("Cannot delete a message that has already been read by the recipient.")

        message.delete()
        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

