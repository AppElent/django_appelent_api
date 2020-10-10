from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers import MeterstandSerializer
from ..models import Meterstand
from ..permissions import IsOwner

class MeterstandViewSet(viewsets.ModelViewSet):
    """
    Meter readings can be used for energy and gas consumption
    """
    queryset = Meterstand.objects.all()
    serializer_class = MeterstandSerializer
    permission_classes = [IsOwner] 
    filterset_fields = ['datetime']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        if getattr(self, 'swagger_fake_view', False):
            return None
        user = self.request.user
        return Meterstand.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = MeterstandSerializer(data=request.data, many=many)
        if serializer.is_valid():
            for meterstand in request.data:
                Meterstand.objects.update_or_create(user=request.user, datetime=meterstand['datetime'], defaults=meterstand)
            #serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

