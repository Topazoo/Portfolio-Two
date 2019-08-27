from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

import mockups.urls
from api.views import http_dispatch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mock/', include(mockups.urls)),
    path('api/', http_dispatch),

    path('', TemplateView.as_view(template_name='home.html')),
]
