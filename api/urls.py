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
router.register('events', EventViewSet, basename='events')
router.register('oauthproviders', OauthProviderViewSet, basename='oauthproviders')
router.register('meterstanden', MeterstandViewSet, basename='meterstanden')
router.register('oauthclients', OAuth2TokenViewSet, basename='oauthclients')
router.register('tado/zones', TadoZone, basename='tado-zones')
router.register('enelogic/buildings', EnelogicBuilding, basename='enelogic-buildings')
router.register('solaredge/sites', SolarEdgeSite, basename='solaredge-sites')

urlpatterns = [
    path('', include(router.urls)),
    path('test1/', test1),
    path('test2/<str:var1>/<int:var2>/', test2),
    path('test3/', TestView.as_view()),
    url(r'^token/', views.obtain_auth_token),
    path('oauth/<str:name>/authorize', authorize),
    path('oauth/<str:name>/authorizationurl', get_authorization_url),
    path('oauth/<str:name>/token', save_access_token),
    path('oauth/<str:name>/refresh', refresh_access_token),
]