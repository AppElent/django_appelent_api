from rest_framework import serializers
from ..models import OauthProvider


class OauthProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthProvider
        #fields = ['id', 'title', 'author']
        fields = "__all__"