from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..serializers import Test1Serializer

from ..modules.oauth import get_session

class EnelogicRequest(viewsets.GenericViewSet):
    serializer_class = Test1Serializer
    _URL = ''

    #def dispatch(self, request, *args, **kwargs):
    #    provider = get_provider('enelogic')
    #    if provider is None:
    #        raise Exception('OauthProvider Enelogic not registered in application. Create entry in OauthProvider table with name=enelogic to resolve this issue.')
    #    return super(EnelogicRequest, self).dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         return None
    #     session = get_session('enelogic', self.request.user)
    #     if session is None:
    #         return None
        
    #     data = session.get(self._URL)
    #     return data

    def get_enelogic_data(self, url):
        session = get_session('enelogic', self.request.user)
        if session is None:
            raise Exception('Session cannot be found')
        data = session.get(url)
        return data

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """
    _URL = '/buildings'

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
