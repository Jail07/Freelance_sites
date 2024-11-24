from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Регистрация маршрутов для ViewSet'ов
router = DefaultRouter()
router.register('profiles', views.ProfileViewSet, basename='profiles')
router.register('skills', views.SkillViewSet, basename='skills')
router.register('messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    # JWT токены
    path('api/account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Аутентификация и регистрация
    path('api/account/login/', views.login_user, name="api-login"),
    path('api/account/register/', views.RegisterUserView.as_view(), name="api-register"),

    # Подключение маршрутов ViewSet'ов
    path('api/', include(router.urls)),

    # Дополнительные маршруты
    path('api/routes/', views.get_routes, name="api-routes"),
]
