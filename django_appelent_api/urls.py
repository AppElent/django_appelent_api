"""django_appelent_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.views.generic.base import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
api_info = openapi.Info(
   title="App-Elent API",
   default_version='v1',
)
schema_view = get_schema_view(
    # openapi.Info(
    #     title="App-Elent API",
    #     default_version='v1',
    #     description="Welcome to the world of App-Elent",
    #     terms_of_service="https://www.jaseci.org",
    #     contact=openapi.Contact(email="jason@jaseci.org"),
    #     license=openapi.License(name="Awesome IP"),
    # ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Get the OPEN-API specification in either JSON or YAML
    re_path(r'^docs(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    # Swagger UI
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'), 
    #ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'), 
    # Admin documentation
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # Admin panel
    path('admin/', admin.site.urls),
    # All API routes
    path('api/', include('api.urls')),
    # All Satisfactory routes
    path('satisfactory/', include('satisfactory.urls')),
    # Add browsable API login/logout views
    path('api-auth/', include('rest_framework.urls')),
    # Redirect empty to /api
    url(r'^$', RedirectView.as_view(url='/api/')),
]
