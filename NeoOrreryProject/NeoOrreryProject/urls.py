from django.contrib import admin  # Import the admin module
from django.urls import path, include
from orrery import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orrery.urls')),
]
