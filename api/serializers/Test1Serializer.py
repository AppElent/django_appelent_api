from rest_framework import serializers

class Test1Serializer(serializers.Serializer):
    var1 = serializers.CharField()
    var2 = serializers.IntegerField()