from django.apps import AppConfig
from django.core.cache import caches

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        try:
            import api.receivers
            #from .singletons import oauth, register_providers
            #register_providers(oauth)
        except expression as identifier:
            pass
