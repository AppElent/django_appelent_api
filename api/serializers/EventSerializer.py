from rest_framework import serializers
from ..models import Event

class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Event
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']