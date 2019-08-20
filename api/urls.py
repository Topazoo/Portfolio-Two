from django.contrib import admin
from django.urls import path, include
import api.views as views

urlpatterns = [
    path('', views.http_dispatch),
]