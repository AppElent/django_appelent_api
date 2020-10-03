from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..serializers import OauthProviderSerializer
from ..models import OauthProvider

class OauthProviderViewSet(viewsets.ModelViewSet):
    queryset = OauthProvider.objects.all()
    serializer_class = OauthProviderSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]