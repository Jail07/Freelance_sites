from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT токены
    path('account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Аутентификация и регистрация
    path('account/login/', views.LoginUserView.as_view(), name="api-login"),
    path('account/register/', views.RegisterUserView.as_view(), name="api-register"),

    path('messages/', views.MessageView.as_view(), name='messages'),
    path('messages/<str:pk>/', views.MessageDeatailView.as_view(), name='message-detail'),

    path('profiles/', views.ProfileView.as_view(), name='profiles'),
    path('profiles/<str:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('skills/', views.SkillView.as_view(), name='skills'),
]
