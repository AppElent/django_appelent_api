from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from ..serializers import Test1Serializer

@api_view(['GET', 'POST'])
def test1(request):
    """
    Simple test
    """
    cache.set('foo', '1 minute', 60)
    cache.set('foo2', '2 minutes', 120)
    cache.set('foo3', '10 seconds', 10)
    cache.set('foo4', '20 seconds', 20)
    cache.set('foo5', 'asd', 120)
    data = {
        "test": True,
        "foo": cache.get('foo')
    }
    print(cache.get('foo'))
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def test2(request, var1, var2):
    """
    Simple test 2
    """
    serializer_class = Test1Serializer

    data = {
        "var1": var1,
        "var2": var2
    }
    serializer = Test1Serializer(data=request.data)
    if serializer.is_valid():
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestView(APIView):
    """
    Test123123o8
    """
    serializer_class = Test1Serializer

    def get(self, request):
        return Response({"success": True})
    
    def post(self, request, format=None):
        serializer = Test1Serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)