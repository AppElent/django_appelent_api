from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..serializers import Test1Serializer

from ..modules.oauth import oauth

class EnelogicRequest(viewsets.GenericViewSet):
    serializer_class = Test1Serializer

    def get_queryset(self):
        return None

    def get_enelogic_data(self, url):
        session = oauth.get_session('enelogic', self.request.user)
        if session is None:
            raise Exception('Session cannot be found')
        data = session.get(url)
        return data

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """

    def list(self, request):
        data = self.get_enelogic_data('/buildings/')
        if data is None:
            return Response('Something went wrong getting the data', status.HTTP_412_PRECONDITION_FAILED)
        return Response(data.json(), status.HTTP_200_OK)

    def retrieve(self, request, pk, format=None):
        data = self.get_enelogic_data('/buildings/' + pk)
        if data is None:
            return Response('Something went wrong getting the data', status.HTTP_412_PRECONDITION_FAILED)
        return Response(data.json(), status.HTTP_200_OK)
