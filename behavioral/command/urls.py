"""
Django URLs for command app.
"""

from django.urls import path, include

app_name = 'command'

urlpatterns = [
    path('api/', include('command.api.urls')),
]
