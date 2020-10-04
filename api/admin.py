from django.contrib import admin
from .models import *

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ['datetime']
    search_fields = ['value', 'application']
    
# @admin.register(Collection)
# class CollectionAdmin(admin.ModelAdmin):
#     filter_horizontal = ['observations']

#admin.site.register(Event)
admin.site.register(Meterstand)
admin.site.register(OauthProvider)
admin.site.register(OAuth2Token)
admin.site.register(TestModel)