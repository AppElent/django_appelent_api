from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from ..models import OAuth2Token
from ..serializers import Test1Serializer
from PyTado.interface import Tado
from django.core.cache import caches
defaultcache = caches['default']

class TadoRequest(viewsets.GenericViewSet):
    """ 
    Class to imcorporate method to make a Tado request 
    """
    serializer_class = Test1Serializer
    _URL = ''

    def get_client(self, request):
        key = 'tado_' + request.user.email
        t = defaultcache.get(key)
        if not t:
            token = OAuth2Token.objects.get(user=request.user, name='tado')
            username = token.access_token.split('/')[0]
            password = token.access_token.split('/')[1]
            t = Tado(username, password)
            defaultcache.set(key, t, 600)
        return t

    def perform_request(self, request, url, **kwargs):
        print(123)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {'id': 1, 'name': 'Woonkamer', 'type': 'HEATING', 'dateCreated': '2017-09-18T19:57:31.720Z', 'deviceTypes': ['RU01'], 'devices': [{'deviceType': 'RU01', 'serialNo': 'RU3927311360', 'shortSerialNo': 'RU3927311360', 'currentFwVersion': '54.19', 'connectionState': {'value': True, 'timestamp': '2020-10-06T12:21:06.972Z'}, 'characteristics': {'capabilities': ['INSIDE_TEMPERATURE_MEASUREMENT', 'IDENTIFY']}, 'batteryState': 'NORMAL', 'duties': ['ZONE_UI', 'CIRCUIT_DRIVER', 'ZONE_LEADER']}], 'reportAvailable': False, 'supportsDazzle': True, 'dazzleEnabled': False, 'dazzleMode': {'supported': True, 'enabled': False}, 'openWindowDetection': {'supported': True, 'enabled': True, 'timeoutInSeconds': 900}}
        print('Running get_queryset')
        t = self.get_client(self.request)
        #return Response(t.getZones())
        data = t._apiCall(self._URL)
        print(data)
        return data


class TadoZone(TadoRequest):
    """
    Get Tado zones
    """
    _URL = 'zones'

    def list(self, request):
        data = self.get_queryset()
        return Response(data)

    def retrieve(self, request, pk, format=None):
        t = self.get_queryset()
        zone = next((x for x in zones if x['id'] == int(pk)), {})
        return Response(zone)

    @action(detail=True, methods=['delete'])
    def overlay(self, request, pk=None, format=None):
        t = self.get_client(request)
        t.resetZoneOverlay(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def overlays(self, request, pk=None, format=None):
        t = self.get_client(request)
        zones = t.getZones()
        for zone in zones:
            t.resetZoneOverlay(zone['id'])
        return Response(status=status.HTTP_204_NO_CONTENT)


# class TadoZoneOverlay(TadoRequest):
#     """
#     Set Tado ZoneOverlay
#     """
#     serializer_class = Test1Serializer
#     _URL = 'zones'
   
#     def list(self, request):
#         data = self.get_queryset()
#         return Response(data)

#     def retrieve(self, request, pk, format=None):
#         t = self.get_queryset()
#         zone = next((x for x in zones if x['id'] == int(pk)), {})
#         return Response(zone)
    
#     def create(self, request):
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def update(self, request, pk, format=None):
#         t = self.get_client(request)
#         #t.setZoneOverlay(pk)
#         return Response(serializer.data)

#     def destroy(self, request, pk, format=None):
#         t = self.get_client(request)
#         t.resetZoneOverlay(pk)
#         return Response(status=status.HTTP_204_NO_CONTENT)

