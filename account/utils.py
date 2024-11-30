from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Profile, Skill

# Пагинация для API
class Pagination(PageNumberPagination):
    page_size = 2  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100

# Поиск профилей
def search_profiles(search_query=None):
    """
    Функция для поиска профилей по имени или навыкам.
    :param search_query: Строка поиска (может быть None).
    :return: Queryset профилей.
    """
    if not search_query:
        return Profile.objects.all()

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(skill__in=skills)
    )
    return profiles
