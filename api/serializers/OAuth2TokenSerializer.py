from rest_framework import serializers
from ..models import OAuth2Token

class OAuth2TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuth2Token
        exclude = ['user']