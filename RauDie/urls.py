# RauDie/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),  # Incluye las URLs de app1 en la raíz del proyecto
]
