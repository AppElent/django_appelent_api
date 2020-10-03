from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..serializers import MeterstandSerializer
from ..models import Meterstand

class MeterstandViewSet(viewsets.ModelViewSet):
    """
    Meter readings can be used for energy and gas consumption
    """
    queryset = Meterstand.objects.all()
    serializer_class = MeterstandSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['datetime']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Meterstand.objects.filter(user=user)