from rest_framework import serializers

class PushoverSerializer(serializers.Serializer):   
    """  Pushover message """
    message = serializers.CharField()
