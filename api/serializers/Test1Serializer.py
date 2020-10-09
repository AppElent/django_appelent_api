from rest_framework import serializers

class Test1Serializer(serializers.Serializer):   
    """  Test """
    var1 = serializers.CharField()
    var2 = serializers.IntegerField()
