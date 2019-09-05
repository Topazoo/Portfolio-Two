from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from api.views import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api),

    path('', TemplateView.as_view(template_name='index.html')),
]
