from rest_framework import serializers
from ..models import Meterstand

class MeterstandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meterstand
        #fields = ['id', 'title', 'author']
        #fields = "__all__"
        exclude = ['user']