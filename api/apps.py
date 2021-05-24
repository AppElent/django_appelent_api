from django.apps import AppConfig
from django.core.cache import caches

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.receivers
