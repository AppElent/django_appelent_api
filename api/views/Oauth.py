from django.http import HttpResponseRedirect
from rest_framework import status, renderers
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from ..serializers import OAuth2TokenSerializer
from ..models import OAuth2Token, Oauth2State
#rom ..singletons import oauth, check_registered
from ..modules.oauth import get_provider, save_token, get_session, update_token
import time

def defaultstate(username):
    return str(username) + "_skjdhfjksdgfkjvbjgvjsdf3497b5v83974yd"

def save_state(name, state):
    stateobject = Oauth2State.objects.create()
    stateobject.state = state
    stateobject.name = name
    stateobject.save()

@api_view(['GET'])
def authorize(request, name):
    provider = get_provider(name)
    if provider is None:
        return Response('Cannot get OauthProvider because ' + name + ' is not set up in OauthProvider table', status=status.HTTP_412_PRECONDITION_FAILED)
    redirect_uri = provider.redirect_uri
    oauth_session = OAuth2Session(provider.client_id, redirect_uri=provider.redirect_uri, scope=provider.default_scope)
    authorization_url, state = oauth_session.authorization_url(provider.authorize_url, state=defaultstate(request.user.id))
    save_state(name, state)
    return HttpResponseRedirect(authorization_url)
    #return oauth.create_client(name).authorize_redirect(request, redirect_uri)
    #return oauth.enelogic.authorize_redirect(request, redirect_uri)

@api_view(['GET'])
def get_authorization_url(request, name):
    provider = get_provider(name)
    if provider is None:
        return Response('Cannot get OauthProvider because ' + name + ' is not set up in OauthProvider table', status=status.HTTP_412_PRECONDITION_FAILED)
    redirect_uri = provider.redirect_uri
    oauth_session = OAuth2Session(provider.client_id, redirect_uri=provider.redirect_uri, scope=provider.default_scope)
    authorization_url, state = oauth_session.authorization_url(provider.authorize_url, state=defaultstate(request.user.id))
    save_state(name, state)
    return Response(authorization_url)

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
@renderer_classes([renderers.JSONRenderer])
def save_access_token(request, name):
    provider = get_provider(name)
    if provider is None:
        return Response('Cannot get OauthProvider because ' + name + ' is not set up in OauthProvider table', status=status.HTTP_412_PRECONDITION_FAILED)
    urlstate = request.query_params.get('state')
    savedstate = Oauth2State.objects.filter(name=name, state=urlstate).first()
    if savedstate is None:
        return Response('Saved state cannot be found', status=status.HTTP_400_BAD_REQUEST)
    savedstate.delete()
    oauth_session = OAuth2Session(provider.client_id, redirect_uri=provider.redirect_uri, scope=provider.default_scope, state=urlstate)
    token = oauth_session.fetch_token(
        provider.access_token_url,
        authorization_response=request.get_full_path(),
        # Google specific extra parameter used for client
        # authentication
        client_secret=provider.client_secret
    )
    result = save_token(name, savedstate.user, token)
    if result is True:
        return Response('Credentials saved successfully. You can close this window.', status=status.HTTP_201_CREATED)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    # try:
    #     instance = OAuth2Token.objects.get(user=savedstate.user, name=name)
    #     serializer = OAuth2TokenSerializer(data=token, instance=instance)
    # except OAuth2Token.DoesNotExist:
    #     serializer = OAuth2TokenSerializer(data=token)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response('Credentials saved successfully. You can close this window.', status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def refresh_access_token(request, name):
    provider = get_provider(name)
    if provider is None:
        return Response('Cannot get OauthProvider because ' + name + ' is not set up in OauthProvider table', status=status.HTTP_412_PRECONDITION_FAILED)
    
    token = OAuth2Token.objects.get(name=name, user=request.user)
    if not token:
        return Response(name + ' token cannnot be found in database', status=status.HTTP_412_PRECONDITION_FAILED)

    session = get_session(name, request.user)
    if not session:
        return Response('Session cannnot be found', status=status.HTTP_412_PRECONDITION_FAILED)

    result = refresh_token(name, request.user, token)
    if result is True:
        return Response('Credentials updated successfully. You can close this window.', status=status.HTTP_201_CREATED)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    