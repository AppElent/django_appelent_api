from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..serializers import Test1Serializer

from ..singletons import oauth, check_registered

class EnelogicRequest(viewsets.GenericViewSet):
    serializer_class = Test1Serializer
    _URL = ''

    def dispatch(self, request, *args, **kwargs):
        registered = check_registered(oauth, 'enelogic')
        if registered == False:
            raise Exception('OauthProvider Enelogic not registered in application. Create entry in OauthProvider table with name=enelogic to resolve this issue.')
        return super(EnelogicRequest, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        client = oauth.create_client('enelogic')
        if client is None:
            return None
        data = oauth.enelogic.get(_URL, request=self.request)
        return data

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """
    _URL = '/api/buildings'

    def list(self, request):
        
        data = self.get_queryset()
        return Response(data.json(), status.HTTP_200_OK)

    def retrieve(self, request, pk, format=None):
        data = oauth.enelogic.get('/api/buildings/' + pk, request=request)
        return Response(data.json(), status.HTTP_200_OK)
