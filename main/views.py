from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import paginateProjects, searchProjects
from .models import Project, Review, Tag
from .serializers import ProjectSerializer, ReviewSerializer
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/main/'},
        {'GET': '/api/main/id'},
        {'POST': '/api/main/id/vote'},
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects, search = searchProjects(request)

    paginated_data = paginateProjects(request, projects)

    serializer = ProjectSerializer(paginated_data["projects"], many=True)

    return Response({
        "projects": serializer.data,
        "current_page": paginated_data["current_page"],
        "total_pages": paginated_data["total_pages"],
        "total_projects": paginated_data["total_projects"],
        "search": search,
    })




@api_view(['GET'])
def getProject(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    user = request.user.profile
    data = request.data
    print(data)

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data['value']
    review.body = data['body']
    review.save()

    project.getVoteCount
    return Response({"detail": "Vote recorded successfully!"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProject(request):
    data = request.data
    try:
        owner = request.user.profile
        title = data.get('title')
        description = data.get('description')
        tags = data.get('tags', [])

        project = Project.objects.create(
            owner=owner,
            title=title,
            description=description,
        )

        # Привязка тегов к проекту
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)

        project.save()
        return Response({"detail": "Project created successfully!"})

    except Exception as e:
        return Response({"detail": f"Didn't give a data or... \n{e}"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProject(request, pk):
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
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    project.delete()
    return Response({"detail": "Project deleted successfully!"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeTag(request):
    tag_id = request.data['tag']
    project_id = request.data['project']

    try:
        project = Project.objects.get(id=project_id)
        tag = Tag.objects.get(id=tag_id)
    except (Project.DoesNotExist, Tag.DoesNotExist):
        return Response({"detail": "Project or Tag not found."}, status=404)

    project.tags.remove(tag)
    return Response({"detail": "Tag removed from project."})
