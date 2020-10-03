from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from ..singletons import oauth
from ..models import OAuth2Token
from PyTado.interface import Tado
from django.core.cache import caches
defaultcache = caches['default']

# def get_tado_client(key):
#     t = defaultcache.get(key)
#     if not t:
#         print('Retrieving value from cahche t1')
#         t = Tado('ericjansen@live.nl', 'r}*dY3qoRM-gqj,_')
#         defaultcache.set(key, t, 600)
#     return t

class TadoRequest(viewsets.ViewSet):
    """ 
    Class to imcorporate method to make a Tado request 
    """

    def get_client(self, request):
        key = 'tado_' + request.user.username
        t = defaultcache.get(key)
        if not t:
            token = OAuth2Token.objects.get(user=request.user, name='tado')
            username = token.access_token_decrypted.split('/')[0]
            password = token.access_token_decrypted.split('/')[1]
            t = Tado(username, password)
            defaultcache.set(key, t, 600)
        return t

    def perform_request(self, request, url, **kwargs):
        print(123)



class TadoZone(TadoRequest):
    """
    Get Tado zones
    """
    def list(self, request):
        t = self.get_client(request)
        #return Response(t.getZones())
        return Response(t._apiCall('zones'))

    def retrieve(self, request, pk, format=None):
        t = self.get_client(request)
        zones = t.getZones()
        zone = next((x for x in zones if x['id'] == int(pk)), {})
        return Response(zone)


class TadoZoneOverlay(TadoRequest):
    """
    Get Tado zones
    """
    def list(self, request):
        t = self.get_client(request)
        return Response(t.getZones())

    def retrieve(self, request, pk, format=None):
        t = self.get_client(request)
        zones = t.getZones()
        zone = next((x for x in zones if x['id'] == int(pk)), {})
        return Response(zone)

    def update(self, request, pk, format=None):
        t = self.get_client(request)
        #t.setZoneOverlay(pk)
        return Response(serializer.data)

    def destroy(self, request, pk, format=None):
        t = self.get_client(request)
        t.resetZoneOverlay(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)