from django.apps import AppConfig


class SingletonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'singleton'
