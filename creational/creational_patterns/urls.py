from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('abstract-factory/', include('abstract_factory.urls')),
]
