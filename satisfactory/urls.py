from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken import views
from .views import *
from rest_framework.routers import DefaultRouter

class OptionalSlashRouter(DefaultRouter):      
    def __init__(self, *args, **kwargs):         
        super(DefaultRouter, self).__init__(*args, **kwargs)         
        self.trailing_slash = '/?' 

router = OptionalSlashRouter('/?')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('products', ProductViewSet, basename='products')
router.register('nodes', NodeViewSet, basename='nodes')
router.register('machinetypes', MachineTypeViewSet, basename='machinetypes')

urlpatterns = [
    path('', include(router.urls)),
]