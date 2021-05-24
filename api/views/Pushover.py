from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
import requests
from ..serializers import PushoverSerializer
from ..modules.oauth import oauth

class PushoverRequest(viewsets.GenericViewSet):
    serializer_class = PushoverSerializer
    url = 'https://api.pushover.net/1/messages.json'

    def get_queryset(self):
        return None

    def send(self, request, message):
        token = oauth.get_token(name='pushover', user=request.user)
        if token is None:
            return Response('SolarEdge token cannot be found', status=status.HTTP_404_NOT_FOUND)
        params = {'token': token.password, 'user': token.username, 'message': message}
        try:
            requests.post(self.url, params)
        except Exception as e:
            return Response('Failed: ' + str(e), status=status.HTTP_412_PRECONDITION_FAILED)
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        try:
            return self.send(request, request.query_params['message'])
        except:
            return Response(None, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        return self.send(request, pk)

    def create(self, request):
        return self.send(request, request.data['message'])

