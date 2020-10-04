from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from ..singletons import oauth, check_registered

class EnelogicRequest(viewsets.ViewSet):

    def dispatch(self, *args, **kwargs):
        print('entering dispatch')
        registered = check_registered(oauth, 'enelogic')
        print(registered)
        if registered == False:
            raise Exception('OauthProvider Enelogic not registered in application. Create entry in OauthProvider table with name=enelogic to resolve this issue.')
        return super(EnelogicRequest, self).dispatch(request, *args, **kwargs)

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """
    def list(self, request):
        print('entering list')
        data = oauth.enelogic.get('/api/buildings', request=request)
        return Response(data.json(), status.HTTP_200_OK)

    def retrieve(self, request, pk, format=None):
        data = oauth.enelogic.get('/api/buildings/' + pk, request=request)
        return Response(data.json(), status.HTTP_200_OK)
