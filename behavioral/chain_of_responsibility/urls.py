from django.urls import path
from .views import FilterEmailAPIView

urlpatterns = [
    path('filter/', FilterEmailAPIView.as_view(), name='mail_filter'),
]
