from django.urls import path
from . import views

urlpatterns = [
    # Маршруты для API
    path('api/', views.getRoutes),  # Получить все доступные API маршруты
    path('api/main/', views.getProjects),  # Получить список всех проектов
    path('api/main/<str:pk>/', views.getProject),  # Получить данные конкретного проекта по ID
    path('api/main/<str:pk>/vote/', views.projectVote),  # Голосование за проект
    path('api/projects/create/', views.createProject),  # Создание нового проекта
    path('api/projects/<str:pk>/update/', views.updateProject),  # Обновление проекта
    path('api/projects/<str:pk>/delete/', views.deleteProject),  # Удаление проекта
    path('api/projects/remove-tag/', views.removeTag),  # Удалить тег из проекта
]
