from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from ..models import OAuth2Token
import requests

class SolarEdgeRequest(viewsets.ViewSet):
    """ 
    Class to imcorporate method to make a request 
    """

    def perform_request(self, request, url, **kwargs):
        token = OAuth2Token.objects.get(user=request.user, name='solaredge')
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        full_url = 'https://monitoringapi.solaredge.com' + url + '?api_key=' + token.access_token_decrypted
        data = requests.get(full_url)
        return Response(data.json())

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
