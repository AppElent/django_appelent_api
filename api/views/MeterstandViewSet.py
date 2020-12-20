from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
            if many:
                for meterstand in request.data:
                    Meterstand.objects.update_or_create(user=request.user, datetime=meterstand['datetime'], defaults=meterstand)
            else:
                #request.data.pop('csrfmiddlewaretoken', None)
                data = {x: request.data[x] for x in request.data if x not in ['csrfmiddlewaretoken']}
                Meterstand.objects.update_or_create(user=request.user, datetime=request.data['datetime'], defaults=data)
            #serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='day/(?P<day>\d{4}-\d{2}-\d{2})/$')#'day/(?P<day>\w+)')
    def day(self, request, day, *args, **kwargs):
        datearray = day.split('-')
        meterstanden = Meterstand.objects.filter(user=self.request.user, datetime__year=datearray[0], datetime__month=datearray[1], datetime__day=datearray[2])
        meterstanden_data = self.get_serializer_class()(meterstanden, many=True)
        return Response(meterstanden_data.data)

    @action(detail=False, methods=['get'], url_path='month/(?P<month>\d{4}-\d{2})/$')
    def month(self, request, month, *args, **kwargs):
        datearray = month.split('-')
        meterstanden = Meterstand.objects.filter(user=self.request.user, datetime__year=datearray[0], datetime__month=datearray[1])
        meterstanden_data = self.get_serializer_class()(meterstanden, many=True)
        return Response(meterstanden_data.data)

