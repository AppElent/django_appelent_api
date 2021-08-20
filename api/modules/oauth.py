from ..models import OauthProvider, OAuth2Token
from ..serializers import OAuth2TokenSerializer
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient, WebApplicationClient
from crum import get_current_user

class CustomOAuth2Session(OAuth2Session):

    def __init__(self, name, user, *args, **kwargs):
        self.provider = self.get_provider(name)
        # If provider is None, raise Error
        if self.provider is None:
            raise Exception('Provider ' + name + ' not found')

        # save settings
        self.name = name
        self.api_base_url = self.provider.api_base_url
        self.user = user
        self.token_serialized = None

        # determine flow
        if self.provider.flow == 'authorization_code':
            # default client
            client = None
        elif self.provider.flow == 'password':
            client = LegacyApplicationClient(client_id=self.provider.client_id)

        # Get token and refresh it if necessary 
        refresh = False
        self.token_from_model = OAuth2Token.objects.get(user=user, name=name)
        self.token_serialized = self.token_from_model.to_token()
        if self.token_from_model is not None:
            if self.token_from_model.expired:
                print('--------------------------Token ' + name + ' is expired --> ' + self.token_from_model.expires_at_string)
                self.token_from_model = OAuth2Token.objects.get(user=user, name=name)
                if self.token_from_model.expired:
                    refresh = True


        # Call OOTB init function
        super().__init__(
            client=client,
            client_id=self.provider.client_id,
            redirect_uri = self.provider.redirect_uri,
            scope=self.provider.default_scope,
            token=self.token_serialized if self.provider.flow == 'authorization_code' else None,
            auto_refresh_url=self.provider.refresh_token_url if self.provider.refresh_token_url else self.provider.access_token_url,
            #auto_refresh_kwargs=self.provider.
            token_updater=self.save_token,
            *args, **kwargs
        ) 

        if refresh:
            pass 
            token = self.refresh_token()
            self.save_token(token)

    #
    # Overrides of the default class
    #
    def authorization_url(self, state=None, *args, **kwargs):
        url = self.provider.authorize_url
        return super(CustomOAuth2Session, self).authorization_url(url, state, *args, **kwargs)

    def fetch_token(self, request, *args, **kwargs):
        url = self.provider.access_token_url
        print('=======================================fetch token is called')
        if self.token.get('access_token'):
            return
        print("==== Token is not set, new one retrieving")
        if self.provider.flow == 'authorization_code':
            token = super(CustomOAuth2Session, self).fetch_token(token_url=url, authorization_response=request.get_full_path(), client_secret=self.provider.client_secret, include_client_id=True, *args, **kwargs)
            self.save_token(token=token)
            print('after', self.token)
        elif self.provider.flow == 'password':
            username = self.token_from_model.username
            password = self.token_from_model.password
            token = super(CustomOAuth2Session, self).fetch_token(token_url=url, username=username, password=password, client_secret=self.provider.client_secret, *args, **kwargs)
        return token

    def get(self, url, *args, **kwargs):
        if not url.lower().startswith('http'):
            url = self.api_base_url + url
        return super(CustomOAuth2Session, self).get(url, *args, **kwargs)

    # def request(self, url, *args, **kwargs):
    #     if not url.lower().startswith('http'):
    #         url = self.api_base_url + url
    #     return super(CustomOAuth2Session, self).request(url, *args, **kwargs)

    #
    # Provider functions (get oauth client details)
    #

    def register_provider(self, provider):
        print('Registering oauthprovider ' + provider.name)
        oauth._providers[provider.name] = provider

    def get_provider(self, name):
        try: 
            provider = oauth._providers[name]
            return provider
        except:
            pass
        try:
            print('Provider ' + name + ' not yet registered. Retrieving from database')
            provider = OauthProvider.objects.get(name=name)
            self.register_provider(provider)
            return provider
        except:
            print('Name does not exist')
            return None
        return provider

    #
    # Token functions (get, update, save)
    #

    # def get_token(self):
    #     token = OAuth2Token.objects.get(user=self.user, name=self.name)
    #     return token

    def save_token(self, token):
        if self.provider.flow == 'authorization_code':
            token['name'] = self.name
            if "." in str(token['expires_at']):
                token['expires_at'] = str(token['expires_at']).split('.')[0]
            
            try:
                instance = OAuth2Token.objects.get(user=self.user, name=self.name)
                serializer = OAuth2TokenSerializer(data=token, instance=instance)
            except OAuth2Token.DoesNotExist:
                serializer = OAuth2TokenSerializer(data=token)
            if serializer.is_valid():
                serializer.save()
                token = OAuth2Token.objects.get(user=self.user, name=self.name)
                self.token_from_model = token
                self.token_serialized = token.to_token()
                self.token = token.to_token()
                return True
            return serializer.errors

    def refresh_token(self, *args, **kwargs):
        if args:
            token = super(CustomOAuth2Session, self).refresh_token(client_id=self.provider.client_id, client_secret=self.provider.client_secret, *args, **kwargs)
        else:
            refresh_token_url = self.provider.refresh_token_url if self.provider.refresh_token_url else self.provider.access_token_url
            token = super(CustomOAuth2Session, self).refresh_token(token_url=refresh_token_url, client_id=self.provider.client_id, client_secret=self.provider.client_secret, *args, **kwargs)
        #token = self.refresh_token(refresh_token_url, client_id=self.provider.client_id, client_secret=self.provider.client_secret)
        #result = self.save_token(token)
        return token
        #return result


class Oauth():
    _sessions = {}
    _providers = {}
    _tokens = {}
    _states = {}

    def get_session(self, name, user, **kwargs):
        try:
            session = self._sessions[user.id][name]
            return session
        except:
            print('--Session not stored. Has to be created')

        session = CustomOAuth2Session(
            name=name, 
            user=user,
            **kwargs
        )
        try:
            self._sessions[user.id][name] = session
        except:
            self._sessions[user.id] = {}
            self._sessions[user.id][name] = session
        return self._sessions[user.id][name]

    def update_token(self, token):
        try:
            oauth._tokens[token.user.id][token.name] = token
        except:
            oauth._tokens[token.user.id] = {}
            oauth._tokens[token.user.id][token.name] = token

    def get_token(self, name, user):
        try:
            token = self._tokens[user.id][name]
            if token.expired:
                self.refresh_token_from_database(name, user)
                token = self._tokens[user.id][name]
                if token.expired:
                    token.delete()
                    return None
            return token
        except:
            print('Token for ' + name + ' is retrieved from database')
            try:
                token = OAuth2Token.objects.get(user=user, name=name)
            except OAuth2Token.DoesNotExist:
                return None
            self.update_token(token)
            return token

    def refresh_token_from_database(self, name, user):
        print('Token for ' + name + ' is updated from database')
        token = OAuth2Token.objects.get(user=user, name=name)
        self.update_token(token)


def register_providers():
    allproviders = OauthProvider.objects.all()
    for provider in allproviders:
        register_provider(provider)


oauth = Oauth()