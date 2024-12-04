from django.urls import path
from .views import ProjectView, ProjectDetailView, TagView, TagDetailView

urlpatterns = [
    # project
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # tags
    path('tags/', TagView.as_view(), name='tag-list'),  # Управление всеми тегами
    path('tags/<str:pk>/', TagDetailView.as_view(), name='tag-detail'),  # Управление конкретным тегом
]
