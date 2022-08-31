from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("health-check", views.healthCheck, name="health-check"),
    path("crop-classification", views.cropClassify, name="crop-classify"),
]
