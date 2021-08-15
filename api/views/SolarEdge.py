from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from ..models import OAuth2Token
from ..serializers import Test1Serializer
from ..modules.oauth import oauth
import requests

class SolarEdgeRequest(viewsets.GenericViewSet):
    """ 
    Class to imcorporate method to make a request
    """
    serializer_class = Test1Serializer

    def perform_request(self, request, url, **kwargs):
        token = oauth.get_token(name='solaredge', user=request.user)  #OAuth2Token.objects.get(user=request.user, name='solaredge')
        if token is None:
            return Response('SolarEdge token cannot be found', status=status.HTTP_404_NOT_FOUND)
        if kwargs is not None and 'params' in kwargs.keys():
            kwargs['params']['api_key'] = token.access_token
        elif kwargs is not None:
            kwargs['params'] = {'api_key': token.access_token}
        else:
            kwargs = {'params': {'api_key': token.access_token}}
        full_url = 'https://monitoringapi.solaredge.com' + url
        data = requests.get(full_url, **kwargs)
        print(data)
        print(data.json())
        return Response(data.json(), status=data.status_code)

    def get_queryset(self):
        return None
        if getattr(self, 'swagger_fake_view', False):
            return None

class SolarEdgeSite(SolarEdgeRequest):
    """
    Get SolarEdge sites
    """

    def list(self, request):
        url = '/sites/list'
        return self.perform_request(request, url)

    def retrieve(self, request, pk, format=None):
        url = '/site/' + pk + '/details'
        return self.perform_request(request, url)

    
