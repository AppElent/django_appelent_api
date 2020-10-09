from rest_framework import viewsets
from ..serializers import OAuth2TokenSerializer
from ..models import OAuth2Token
from ..permissions import IsOwner

class OAuth2TokenViewSet(viewsets.ModelViewSet):
    queryset = OAuth2Token.objects.all()
    serializer_class = OAuth2TokenSerializer 
    permission_classes = [IsOwner]
    