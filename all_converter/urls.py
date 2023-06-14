from django.urls import path
from . import views

urlpatterns = [
    path('', views.converter_png, name='converter-png'),
    path('download_images/', views.download_images, name='download_images'),
]
