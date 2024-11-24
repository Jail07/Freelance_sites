from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, Review, Tag
from .serializers import ProjectSerializer, ReviewSerializer
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    """
    Функция для получения всех доступных API маршрутов.
    """
    routes = [
        {'GET': '/api/main/'},  # Получить все проекты
        {'GET': '/api/main/id'},  # Получить конкретный проект по id
        {'POST': '/api/main/id/vote'},  # Отдать голос за проект

        {'POST': '/api/account/token'},  # Получить токен пользователя
        {'POST': '/api/account/token/refresh'},  # Обновить токен
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    """
    Получить список всех проектов.
    """
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    """
    Получить данные о конкретном проекте по ID.
    """
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    """
    Голосование за проект.
    """
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data['value']  # "up" or "down"
    review.save()

    project.getVoteCount  # Обновление подсчета голосов
    return Response({"detail": "Vote recorded successfully!"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProject(request):
    """
    Создать новый проект.
    """
    data = request.data

    owner = request.user.profile
    title = data.get('title')
    description = data.get('description')
    demo_link = data.get('demo_link')
    source_link = data.get('source_link')
    tags = data.get('tags', [])

    project = Project.objects.create(
        owner=owner,
        title=title,
        description=description,
        demo_link=demo_link,
        source_link=source_link,
    )

    # Привязка тегов к проекту
    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        project.tags.add(tag)

    project.save()

    return Response({"detail": "Project created successfully!"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProject(request, pk):
    """
    Обновить проект.
    """
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    data = request.data

    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.demo_link = data.get('demo_link', project.demo_link)
    project.source_link = data.get('source_link', project.source_link)
    project.save()

    tags = data.get('tags', [])
    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        project.tags.add(tag)

    project.save()

    return Response({"detail": "Project updated successfully!"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProject(request, pk):
    """
    Удалить проект.
    """
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    project.delete()
    return Response({"detail": "Project deleted successfully!"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeTag(request):
    """
    Удалить тег из проекта.
    """
    tag_id = request.data['tag']
    project_id = request.data['project']

    try:
        project = Project.objects.get(id=project_id)
        tag = Tag.objects.get(id=tag_id)
    except (Project.DoesNotExist, Tag.DoesNotExist):
        return Response({"detail": "Project or Tag not found."}, status=404)

    project.tags.remove(tag)
    return Response({"detail": "Tag removed from project."})
