from ..models import OauthProvider, OAuth2Token
from ..serializers import OAuth2TokenSerializer
from requests_oauthlib import OAuth2Session
from crum import get_current_user

def fetch_token(name, request):
    token = OAuth2Token.objects.get(
        name=name,
        user=request.user
    )
    print('token is being fetched from the database')
    return token.to_token()

class CustomOAuth2Session(OAuth2Session):

    def __init__(self, name, api_base_url, *args, **kwargs):
        self.name = name
        self.api_base_url = api_base_url
        super().__init__(*args, **kwargs) 

    def get(self, url, *args, **kwargs):
        print(0, url)
        if not url.lower().startswith('http'):
            url = self.api_base_url + url
        print(1, url)
        return super(CustomOAuth2Session, self).get(url, *args, **kwargs)

class Oauth():
    _sessions = {}
    _endpoints = {}
    _providers = {}
    _tokens = {}

def get_provider(name):
    try: 
        provider = oauth._providers[name]
        return provider
    except:
        pass
    try:
        provider = OauthProvider.objects.get(name=name)
        register_provider(provider)
        return provider
    except:
        print('Name does not exist')
        return None
    return None

def save_token(name, user, token):
    print('Token is being saved', token, token['expires_at'])
    token['name'] = name
    if "." in str(token['expires_at']):
        token['expires_at'] = str(token['expires_at']).split('.')[0]
    
    try:
        instance = OAuth2Token.objects.get(user=user, name=name)
        serializer = OAuth2TokenSerializer(data=token, instance=instance)
    except OAuth2Token.DoesNotExist:
        serializer = OAuth2TokenSerializer(data=token)
    if serializer.is_valid():
        serializer.save()
        return True
    return serializer.errors

def update_token(name, user, token):
    provider = get_provider(name)
    refresh_token_url = provider.refresh_token_url if provider.refresh_token_url else provider.access_token_url
    token = session.refresh_token(refresh_token_url, client_id=provider.client_id, client_secret=provider.client_secret)
    result = save_token(name, user, token)
    return result

def get_session(name, user, **kwargs):
    provider = get_provider(name)
    token = get_token(name, user)
    if token is None or provider is None:
        return None
    if token.expired:
        print('--------------------------Token ' + name + ' is expired --> ' + token.expires_at_string)
        token = OAuth2Token.objects.get(user=user, name=name)
        if token.expired:
            update_token(name, user, token)

    print('Token', token)
    session = CustomOAuth2Session(
        name=name, 
        api_base_url=provider.api_base_url, 
        client_id=provider.client_id, 
        token=token.to_token(), 
        #auto_refresh_url=provider.refresh_token_url if provider.refresh_token_url else provider.access_token_url, 
        #auto_refresh_kwargs=provider.refresh_token_params if provider.refresh_token_params else None,
        #token_updater=save_token(name, user), 
        **kwargs
    )
    return session

def get_token(name, user):
    try:
        token = oauth._tokens[user.id][name]
        return token
    except:
        print('--Token is retrieved from database')
        token = OAuth2Token.objects.get(user=user, name=name)
        try:
            oauth._tokens[user.id][name] = token
        except:
            oauth._tokens[user.id] = {}
            oauth._tokens[user.id][name] = token
        return token
    

def register_provider(provider):
    print('Registering oauthprovider ' + provider.name)
    oauth._providers[provider.name] = provider
    """
    if provider.flow == 'password':
        print('password flow for ', provider.name)
        oauth_sessions._sessions[provider.name] = OAuth2Session(provider.client_id, provider.client_secret, scope=eval(provider.client_kwargs)['scope'])
        oauth_sessions._endpoints[provider.name] = provider.access_token_url
    else:
        print('registreren met', provider.client_id)
        oauth_sessions._providers[provider.name] = provider
        oauth.register(
            name=provider.name,
            client_id=provider.client_id,
            client_secret=provider.client_secret,
            access_token_url=provider.access_token_url,
            access_token_params=provider.access_token_params,
            authorize_url=provider.authorize_url,
            authorize_params=provider.authorize_params,
            api_base_url=provider.api_base_url,
            client_kwargs=eval(provider.client_kwargs),
        )
    """

def register_providers():
    allproviders = OauthProvider.objects.all()
    for provider in allproviders:
        register_provider(provider)


oauth = Oauth()