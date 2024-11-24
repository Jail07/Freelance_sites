from django.contrib import admin
from django.urls import path, include

# Путь для документации API через Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Freelance Platform API",
        default_version='v1',
        description="API для платформы фрилансеров",
        contact=openapi.Contact(email="contact@freelance.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    # Убедитесь, что используется правильный класс генератора
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('', include('account.urls')),

    # Swagger документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]