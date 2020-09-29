from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, Meterstand, OauthProvider
from .serializers import EventSerializer, MeterstandSerializer, OauthProviderSerializer, Test1Serializer

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """
    Events can be used for logging or notification purposes
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ('category', 'application', 'severity')
    ordering_fields = ['category', 'severity']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Event.objects.filter(user=user)

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

class OauthProviderViewSet(viewsets.ModelViewSet):
    queryset = OauthProvider.objects.all()
    serializer_class = OauthProviderSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        new_credentials = "test" + serializer.validated_data['credentials']
        serializer.save(credentials=new_credentials)

@api_view(['GET', 'POST'])
def test1(request):
    """
    Simple test
    """
    data = {
        "test": True
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def test2(request, var1, var2):
    """
    Simple test 2
    """
    serializer_class = Test1Serializer

    data = {
        "var1": var1,
        "var2": var2
    }
    serializer = Test1Serializer(data=request.data)
    if serializer.is_valid():
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestView(APIView):
    """
    Test123123o8
    """
    serializer_class = Test1Serializer

    def get(self, request):
        return Response({"success": True})
    
    def post(self, request, format=None):
        serializer = Test1Serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
