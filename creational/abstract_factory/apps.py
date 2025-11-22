from django.apps import AppConfig


class AbstractFactoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abstract_factory'
