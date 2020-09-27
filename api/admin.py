from django.contrib import admin
from .models import Event, Meterstand, OauthProvider

# Register your models here.
admin.site.register(Event)
admin.site.register(Meterstand)
admin.site.register(OauthProvider)