from django.urls import path
from . import views

urlpatterns = [
    path('', views.converter_png, name='converter-png'),
    path('download_images/', views.download_images, name='download-images'),
    path('merge_pdf/', views.merge_pdf, name='merge-pdf'),
    #path('download_pdf/', views.download_pdf, name = 'download_pdf'),
]
