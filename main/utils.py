from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))

    paginator = Paginator(projects, size)

    try:
        paginated_projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        paginated_projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        paginated_projects = paginator.page(page)

    return {
        "projects": paginated_projects.object_list,
        "current_page": page,
        "total_pages": paginator.num_pages,
        "total_projects": paginator.count,
    }



def searchProjects(request):
    search = request.GET.get('search', '')

    tags = Tag.objects.filter(name__icontains=search)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        Q(owner__name__icontains=search) |
        Q(tags__in=tags)
    )

    return projects, search
