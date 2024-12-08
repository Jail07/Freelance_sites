from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404

from account.models import Profile
from .utils import paginateProjects, searchProjects
from .models import Project, Tag, Review, Bids
from .serializers import ProjectSerializer, TagSerializer, BidSerializer, ReviewSerializer


class ProjectView(APIView):
    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        projects, search_query = searchProjects(request)
        paginated_data = paginateProjects(request, projects)


        serializer = ProjectSerializer(paginated_data["projects"], many=True)
        return Response({
            "projects": serializer.data,
            "current_page": request.GET.get('page', 1),
            "search_query": search_query,
            "total_projects": len(projects),
        })

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer},
    )
    def post(self, request):
        try:
            owner = request.user.profile
            data = request.data

            project = Project.objects.create(
                owner=owner,
                title=data.get('title'),
                description=data.get('description'),
            )

            tags = data.get('tags', [])
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

            project.save()
            serializer = ProjectSerializer(project, many=False)
            return Response(serializer.data, status=201)
        except:
            return Response(serializer.error, status=405)


class ProjectDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)

        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={200: ProjectSerializer},
    )
    def put(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        data = request.data

        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)

        project.save()

        tags = data.get('tags', [])
        if tags:
            project.tags.clear()
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Удалить проект.
        """
        project = get_object_or_404(Project, id=pk)
        project.delete()
        return Response({"detail": "Project deleted successfully!"}, status=204)


class ReviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reviews = Review.objects.filter(project__id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        response={200: ReviewSerializer}
    )
    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=404)
        user = self.request.user.profile
        data = self.request.data
        print(data)
        review, created = Review.objects.get_or_create(
            owner=user,
            project=project,
        )
        review.value = data['value']
        review.body = data['body']
        review.save()
        project.getVoteCount
        return Response({"detail": "Review recorded successfully!"})


class TagView(APIView):
    """
    API для управления тегами.
    """
    permission_classes = [IsAuthenticated]  # Доступ только для администраторов

    def get(self, request):
        """
        Получить список всех тегов.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=TagSerializer,
        responses={201: TagSerializer}
    )
    def post(self, request):
        """
        Создать новый тег.
        """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TagDetailView(APIView):
    """
    API для управления конкретным тегом.
    """
    permission_classes = [IsAdminUser]  # Доступ только для администраторов

    @swagger_auto_schema(
        request_body=TagSerializer,
        responses={200: TagSerializer}
    )
    def put(self, request, pk):
        """
        Обновить тег.
        """
        tag = get_object_or_404(Tag, id=pk)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """
        Удалить тег.
        """
        tag = get_object_or_404(Tag, id=pk)
        tag.delete()
        return Response({"detail": "Tag deleted successfully!"}, status=204)


class BidListView(APIView):
    """Просмотр всех заявок, созданных текущим пользователем"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bids = Bids.objects.filter(sender=request.user.profile)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)


class ProjectBidsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response({'detail': 'Проект не найден'}, status=status.HTTP_404_NOT_FOUND)

        if project.owner != request.user.profile:
            return Response({'detail': 'Нет доступа к заявкам этого проекта'}, status=status.HTTP_403_FORBIDDEN)

        # Получаем все заявки, связанные с проектом
        bids = Bids.objects.filter(project=project)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BidSerializer,
        responses={200: BidSerializer}
    )
    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=404)
        user = self.request.user.profile
        data = self.request.data
        print(data)
        review, created = Bids.objects.get_or_create(
            sender=user,
            project=project,
        )
        review.subject = data['subject']
        review.body = data['body']
        review.save()
        return Response({"detail": "Bid send successfully!"})


class AddTeamMemberView(APIView):
    """Добавление пользователя в проект по username"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer},
    )
    def put(self, request, pk):
        project = Project.objects.get(id=pk)
        if project.owner != request.user.profile:
            return Response({'detail': 'Нет доступа'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        try:
            profile = Profile.objects.get(user__username=username)
            project.add_team_member(profile)
            return Response({'detail': 'Участник добавлен'})
        except Profile.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
