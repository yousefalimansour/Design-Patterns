from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chain/', include('chain_of_responsibility.urls')),
]
