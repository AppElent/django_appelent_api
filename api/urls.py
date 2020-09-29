from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('oauthproviders', OauthProviderViewSet, basename='oauthproviders')
router.register('meterstanden', MeterstandViewSet, basename='meterstanden')

urlpatterns = [
    path('', include(router.urls)),
    path('test1/', test1),
    path('test2/<str:var1>/<int:var2>/', test2),
    path('test3/', TestView.as_view()),
    url(r'^api-token/', views.obtain_auth_token),
]