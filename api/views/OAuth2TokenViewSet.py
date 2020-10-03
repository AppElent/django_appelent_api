from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..serializers import OAuth2TokenSerializer
from ..models import OAuth2Token

class OAuth2TokenViewSet(viewsets.ModelViewSet):
    queryset = OAuth2Token.objects.all()
    serializer_class = OAuth2TokenSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]