from django.urls import path, include
from .views import EventViewSet, MeterstandViewSet, OauthProviderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('oauthproviders', OauthProviderViewSet, basename='oauthproviders')
router.register('meterstanden', MeterstandViewSet, basename='meterstanden')

urlpatterns = [
    path('', include(router.urls)),
]