from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('home/$', TemplateView.as_view(template_name='home-mock.html')),
]