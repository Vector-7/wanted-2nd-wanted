from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

URI = 'api'


schema_view = get_schema_view(
    openapi.Info(
        title="Wanted 5주차 과제",
        default_version='1.0',
        description='Wanted 5주차 과제 API',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_url = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{URI}/auth/', include('access.urls')),
    path(f'{URI}/users', include('user.urls')),
    path(f'{URI}/companies', include('company.urls')),
] + swagger_url
