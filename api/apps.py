from django.apps import AppConfig
from authlib.integrations.django_client import OAuth
from django.core.cache import caches

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.receivers
        from .singletons import oauth, register_providers
        register_providers(oauth)
        # defaultcache = caches['default']
        # from .modules.oauth import fetch_token
        # from .models import OauthProvider, OAuth2Token
        # from .singleton import oauth, register

        # print(oauth)
        # register()
        # print(oauth)

        # oauth = OAuth(fetch_token=fetch_token)
        # print('settings oauthproviders')
        # allproviders = OauthProvider.objects.all()
        # for provider in allproviders:
        #     oauth.register(
        #         name=provider.name,
        #         client_id=provider.client_id,
        #         client_secret=provider.client_secret_decrypted,
        #         access_token_url=provider.access_token_url,
        #         access_token_params=provider.access_token_params,
        #         authorize_url=provider.authorize_url,
        #         authorize_params=provider.authorize_params,
        #         api_base_url=provider.api_base_url,
        #         client_kwargs=eval(provider.client_kwargs),
        #     )

        # print(OAuth2Token.objects.get(name='enelogic'))
        # print(oauth.enelogic.create_authorization_url('test123'))
        # defaultcache.set('oauth', oauth)
        # #defaultcache.get('oauth')
