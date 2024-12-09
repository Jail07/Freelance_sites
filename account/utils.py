from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination

from .models import Profile, Skill

class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

def paginateProfile(request, profiles):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 2))

    paginator = Paginator(profiles, size)

    try:
        paginated_profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        paginated_profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        paginated_profiles = paginator.page(page)

    return {
        "profiles": paginated_profiles.object_list,
        "current_page": page,
        "total_pages": paginator.num_pages,
        "total_profiles": paginator.count,
    }


def search_profiles(request):
    search = request.GET.get('search', '')

    skills = Skill.objects.filter(name__icontains=search)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search) |
        Q(surname__icontains=search) |
        Q(location__icontains=search) |
        Q(skills__in=skills)
    )

    return profiles, search