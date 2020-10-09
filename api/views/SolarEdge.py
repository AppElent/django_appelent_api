from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from ..models import OAuth2Token
from ..serializers import Test1Serializer
import requests

class SolarEdgeRequest(viewsets.GenericViewSet):
    """ 
    Class to imcorporate method to make a request 
    """
    serializer_class = Test1Serializer
    _URL = ''

    def perform_request(self, request, url, **kwargs):
        token = OAuth2Token.objects.get(user=request.user, name='solaredge')
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        full_url = 'https://monitoringapi.solaredge.com' + url + '?api_key=' + token.access_token
        data = requests.get(full_url)
        print(data.json())
        return Response(data.json(), status=data.status_code)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return self.perform_request(self.request, self._URL)

class SolarEdgeSite(SolarEdgeRequest):
    """
    Get SolarEdge sites
    """
    _URL = '/sites/list'

    def list(self, request):
        return self.get_queryset()

    def retrieve(self, request, pk, format=None):
        url = '/site/' + pk + '/details'
        return self.perform_request(request, url)
