from django.contrib import admin
from .models import *

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ['datetime']
    search_fields = ['value', 'application']

@admin.register(OAuth2Token)
class OAuth2TokenAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['value', 'application']
    readonly_fields = ['expires_at_string']
    
# @admin.register(Collection)
# class CollectionAdmin(admin.ModelAdmin):
#     filter_horizontal = ['observations']

#admin.site.register(Event)
admin.site.register(Meterstand)
admin.site.register(OauthProvider)
admin.site.register(TestModel)