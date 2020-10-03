from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from ..singletons import oauth

class EnelogicRequest(viewsets.ViewSet):

    def request():
        print(123)

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """
    def list(self, request):
        data = oauth.enelogic.get('/api/buildings', request=request)
        return Response(data.json(), status.HTTP_200_OK)

    def retrieve(self, request, pk, format=None):
        data = oauth.enelogic.get('/api/buildings/' + pk, request=request)
        return Response(data.json(), status.HTTP_200_OK)
