from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

import mockups.urls
from api.views import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mock/', include(mockups.urls)),
    path('api/', api),

    path('', TemplateView.as_view(template_name='home.html')),
]
