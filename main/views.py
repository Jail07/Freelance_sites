from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404

from .utils import paginateProjects, searchProjects
from .models import Project, Tag, Review
from .serializers import ProjectSerializer, TagSerializer


class ProjectView(APIView):
    """
    API для работы с проектами.
    """

    def get_permissions(self):
        """
        Определяем разрешения на основе HTTP-метода.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """
        Получить список проектов с фильтрацией, пагинацией и поиском.
        """
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
        """
        Создать новый проект.
        """
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

class ProjectDetailView(APIView):
    """
    API для управления конкретным проектом.
    """

    def get_permissions(self):
        """
        Определяем разрешения на основе HTTP-метода.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        """
        Получить данные о конкретном проекте.
        """
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={200: ProjectSerializer},
    )
    def put(self, request, pk):
        """
        Обновить данные проекта.
        """
        project = get_object_or_404(Project, id=pk)
        data = request.data

        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.demo_link = data.get('demo_link', project.demo_link)
        project.source_link = data.get('source_link', project.source_link)

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


class TagView(APIView):
    """
    API для управления тегами.
    """
    permission_classes = [IsAdminUser]  # Доступ только для администраторов

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