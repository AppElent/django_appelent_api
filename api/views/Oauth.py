from django.http import HttpResponseRedirect
from django.core.cache import cache
from rest_framework import status, renderers
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from ..serializers import OAuth2TokenSerializer
from ..models import OAuth2Token
from django.contrib.auth import get_user_model
#rom ..singletons import oauth, check_registered
from ..modules.oauth import oauth
import time, traceback
User = get_user_model()

@api_view(['GET'])
def authorize(request, name):
    try:
        session = oauth.get_session(name, request.user)
        print(session.token_from_model)
    except Exception as e:
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)

    authorization_url, state = session.authorization_url()
    cache.set('oauthstates.' + state, request.user.id, 120)
    return HttpResponseRedirect(authorization_url)

@api_view(['GET'])
def get_authorization_url(request, name):
    try:
        session = oauth.get_session(name, request.user)
        print(session.token_from_model)
    except Exception as e:
        print(traceback.format_exc())
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)
    
    authorization_url, state = session.authorization_url()
    cache.set('oauthstates.' + state, request.user.id, 120)
    return Response(authorization_url)

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
@renderer_classes([renderers.JSONRenderer])
def save_access_token(request, name):
    urlstate = request.query_params.get('state')
    user_id = cache.get('oauthstates.' + urlstate)
    user = User.objects.get(id=user_id)
    if user is None:
        return Response('Saved state cannot be found', status=status.HTTP_400_BAD_REQUEST)

    cache.delete('oauthstates.' + urlstate)
    try:
        session = oauth.get_session(name=name, user=user)
    except Exception as e:
        print(traceback.format_exc())
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)
    
    try:
        token = session.fetch_token(request=request )
        return Response('Credentials saved successfully. You can close this window.', status=status.HTTP_201_CREATED)
    except Exception as e:
        print(traceback.format_exc())
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)

@api_view(['GET', 'POST'])
def refresh_access_token(request, name):
    try:
        session = oauth.get_session(name=name, user=request.user)
    except Exception as e:
        print(traceback.format_exc())
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)

    try:
        token = session.refresh_token()
        return Response('Credentials updated successfully. You can close this window.', status=status.HTTP_201_CREATED)
    except Exception as e:
        print(traceback.format_exc())
        return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)
    
    