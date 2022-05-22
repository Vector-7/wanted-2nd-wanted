from django.contrib import admin
from django.urls import path, include

URI = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{URI}/auth/', include('access.urls')),
]
