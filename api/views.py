from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Event, Meterstand, OauthProvider
from .serializers import EventSerializer, MeterstandSerializer, OauthProviderSerializer

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class MeterstandViewSet(viewsets.ModelViewSet):
    queryset = Meterstand.objects.all()
    serializer_class = MeterstandSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class OauthProviderViewSet(viewsets.ModelViewSet):
    queryset = OauthProvider.objects.all()
    serializer_class = OauthProviderSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        new_credentials = "test" + serializer.validated_data['credentials']
        serializer.save(credentials=new_credentials)