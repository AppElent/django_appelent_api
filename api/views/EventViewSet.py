from rest_framework import viewsets
from rest_framework.response import Response
from ..serializers import EventSerializer
from ..models import Event
from ..permissions import IsOwner

class EventViewSet(viewsets.ModelViewSet):
    """
    Events can be used for logging or notification purposes
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    permission_classes = [IsOwner]
    filterset_fields = ('category', 'application', 'severity')
    ordering_fields = ['category', 'severity']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        if getattr(self, 'swagger_fake_view', False):
            return None
        user = self.request.user
        return Event.objects.filter(user=user)
