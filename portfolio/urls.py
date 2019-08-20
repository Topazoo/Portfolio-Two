from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

import mockups.urls, api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mock/', include(mockups.urls)),
    path('api/', include(api.urls)),

    path('', TemplateView.as_view(template_name='home.html')),
]
