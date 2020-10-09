from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers import OauthProviderSerializer
from ..models import OauthProvider

class OauthProviderViewSet(viewsets.ModelViewSet):
    queryset = OauthProvider.objects.all()
    serializer_class = OauthProviderSerializer 
    permission_classes = [IsAdminUser]