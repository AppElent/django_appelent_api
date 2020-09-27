from rest_framework import serializers
from .models import Event, Meterstand, OauthProvider

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        #fields = ['id', 'title', 'author']
        fields = "__all__"

class OauthProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthProvider
        #fields = ['id', 'title', 'author']
        fields = "__all__"


class MeterstandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meterstand
        #fields = ['id', 'title', 'author']
        fields = "__all__"