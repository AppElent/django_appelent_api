from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..serializers import EventSerializer
from ..models import Event

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