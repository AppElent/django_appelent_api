from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.cache import cache
from datetime import datetime, timedelta
from ..serializers import Test1Serializer

from ..modules.oauth import oauth

class EnelogicRequest(viewsets.GenericViewSet):
    serializer_class = Test1Serializer

    def get_queryset(self):
        return None

    def get_enelogic_data(self, url):
        session = oauth.get_session('enelogic', self.request.user)
        if session is None:
            raise Exception('Session cannot be found')
        data = session.get(url)
        return data

    def get_measuringpoint(self):
        cachekey = f'users#{self.request.user.id}:enelogic:measuringpoint'
        measuringpoint = cache.get(cachekey)
        if measuringpoint is not None:
            return measuringpoint
        data = self.get_enelogic_data('/measuringpoints')
        measuringpoint = data.json()[0]
        cache.set(cachekey, measuringpoint)
        return measuringpoint

class EnelogicBuilding(EnelogicRequest):
    """
    Get Enelogic buildings
    """

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

class EnelogicMeasuringPoints(EnelogicRequest):
    """
    Get Enelogic Measuring points
    """

    def list(self, request):
        data = self.get_measuringpoint('/measuringpoints')
        if data is None:
            return Response('Something went wrong getting the data', status.HTTP_412_PRECONDITION_FAILED)
        return Response(data.json(), status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        data = self.get_enelogic_data('/measuringpoints/' + pk)
        if data is None:
            return Response('Something went wrong getting the data', status.HTTP_412_PRECONDITION_FAILED)
        return Response(data.json(), status.HTTP_200_OK)


class EnelogicDataPoints(EnelogicRequest):
    """
    Get Enelogic data points
    """

    def list(self, request, **kwargs):
        measuringpoint = self.get_measuringpoint()
        measuringpointid = measuringpoint['id']
        date = request.GET.get('date')
        if date is None:
            date = (datetime.today() - timedelta(days=2))
        else:
            date = datetime.strptime(date, '%Y-%m-%d')
        dayfrom = datetime.strftime(date, '%Y-%m-%d')
        dayto= datetime.strftime(date + timedelta(days=1), '%Y-%m-%d')
        data = self.get_enelogic_data(f'/measuringpoints/{measuringpointid}/datapoints/{dayfrom}/{dayto}')
        return Response(data.json(), status.HTTP_200_OK)

class EnelogicDataPointsDays(EnelogicRequest):
    """
    Get Enelogic data points days
    """

    def list(self, request, **kwargs):
        measuringpoint = self.get_measuringpoint()
        measuringpointid = measuringpoint['id']
        dayfrom = request.GET.get('dayfrom')
        if dayfrom is None:
            dayfrom = (datetime.today() - timedelta(days=31))
        else:
            dayfrom = datetime.strptime(dayfrom, '%Y-%m-%d')
        dayfrom = datetime.strftime(dayfrom, '%Y-%m-%d')
        dayto = request.GET.get('dayto')
        if dayto is None:
            dayto = (datetime.today())
        else:
            dayto = datetime.strptime(dayto, '%Y-%m-%d')
        dayto = datetime.strftime(dayto, '%Y-%m-%d')
        data = self.get_enelogic_data(f'/measuringpoints/{measuringpointid}/datapoint/days/{dayfrom}/{dayto}')
        return Response(data.json(), status.HTTP_200_OK)

class EnelogicDataPointsMonths(EnelogicRequest):
    """
    Get Enelogic data points days
    """

    def list(self, request, **kwargs):
        measuringpoint = self.get_measuringpoint()
        measuringpointid = measuringpoint['id']
        dayfrom = request.GET.get('dayfrom')
        if dayfrom is None:
            dayfrom = (datetime.today() - timedelta(days=365))
        else:
            dayfrom = datetime.strptime(dayfrom, '%Y-%m')
        dayfrom = datetime.strftime(dayfrom, '%Y-%m')
        dayto = request.GET.get('dayto')
        if dayto is None:
            dayto = (datetime.today())
        else:
            dayto = datetime.strptime(dayto, '%Y-%m')
        dayto = datetime.strftime(dayto, '%Y-%m')
        data = self.get_enelogic_data(f'/measuringpoints/{measuringpointid}/datapoint/months/{dayfrom}-01/{dayto}-01')
        return Response(data.json(), status.HTTP_200_OK)