from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Meterstand)
admin.site.register(OauthProvider)
admin.site.register(OAuth2Token)