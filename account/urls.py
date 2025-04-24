from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/login/', views.LoginUserView.as_view(), name="api-login"),
    path('auth/logout/', views.LogoutUserView.as_view(), name="api-logout"),
    path('auth/register/', views.RegisterUserView.as_view(), name="api-register"),

    path('messages/', views.MessageView.as_view(), name='messages'),
    path('messages/<str:pk>/', views.MessageDeatailView.as_view(), name='message-detail'),

    path('profiles/', views.ProfileView.as_view(), name='profiles'),
    path('profiles/<str:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('my-profile/', views.MyProfileDetailView.as_view(), name='my-profile-detail'),
    path('skills/', views.SkillView.as_view(), name='skills'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

