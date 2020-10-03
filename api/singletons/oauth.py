from authlib.integrations.django_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from ..models import OauthProvider, OAuth2Token

def fetch_token(name, request):
    token = OAuth2Token.objects.get(
        name=name,
        user=request.user
    )
    print('token is being fetched from the database')
    return token.to_token()

class OauthSessions():
    _sessions = {}
    _endpoints = {}

def register_providers(oauth):
    print('settings oauthproviders')
    allproviders = OauthProvider.objects.all()
    for provider in allproviders:
        if provider.flow == 'password':
            print('password flow for ', provider.name)
            oauth_sessions._sessions[provider.name] = OAuth2Session(provider.client_id, provider.client_secret, scope=eval(provider.client_kwargs)['scope'])
            oauth_sessions._endpoints[provider.name] = provider.access_token_url
        else:
            oauth.register(
                name=provider.name,
                client_id=provider.client_id,
                client_secret=provider.client_secret_decrypted,
                access_token_url=provider.access_token_url,
                access_token_params=provider.access_token_params,
                authorize_url=provider.authorize_url,
                authorize_params=provider.authorize_params,
                api_base_url=provider.api_base_url,
                client_kwargs=eval(provider.client_kwargs),
            )

oauth = OAuth(fetch_token=fetch_token)
oauth_sessions = OauthSessions()