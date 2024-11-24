from django.urls import path
from . import views


urlpatterns = [
    path('api/', views.getRoutes),
    path('api/main/', views.getProjects),
    path('api/main/<str:pk>/', views.getProject),
    path('api/main/<str:pk>/vote/', views.projectVote),

    path('remove-tag/', views.removeTag),

    path('', views.projects, name='main'),
    path('create-project/', views.createProject, name='create-project'),
    path('update-project/<str:pk>', views.updateProject, name='update-project'),
    path('delete-project/<str:pk>', views.deleteProject, name='delete-project'),
    path('<str:pk>/', views.project, name='project'),
]
