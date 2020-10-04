from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import OAuth2TokenSerializer
from ..models import OAuth2Token
from ..singletons import oauth, check_registered

@api_view(['GET'])
def authorize(request, name):
    registered = check_registered(oauth, name)
    redirect_uri = 'http://localhost:8000/api/oauth/' + name + '/token'
    return oauth.create_client(name).authorize_redirect(request, redirect_uri)
    #return oauth.enelogic.authorize_redirect(request, redirect_uri)

@api_view(['GET'])
def save_access_token(request, name):
    registered = check_registered(oauth, name)
    token = oauth.create_client(name).authorize_access_token(request)
    token["name"] = name
    try:
        instance = OAuth2Token.objects.get(user=request.user, name=name)
        serializer = OAuth2TokenSerializer(data=token, instance=instance)
    except OAuth2Token.DoesNotExist:
        serializer = OAuth2TokenSerializer(data=token)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)