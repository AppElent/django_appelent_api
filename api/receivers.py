from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from .models import OAuth2Token
from .modules.oauth import oauth

@receiver(post_save, dispatch_uid="test_receiver")
def test(**kwargs):
    print('Dit dan wel')

@receiver(post_save, sender=OAuth2Token, dispatch_uid="save_oauth_token")
def token_saved(sender, instance, **kwargs):
    oauth.update_token(instance)
    cache.set(userid=instance.user.id, category='tokens', key=instance.name, value=instance)
    cache.delete(userid=instance.user.id, category=instance.name)
    print(cache._cache)

@receiver(post_delete, sender=OAuth2Token, dispatch_uid="delete_oauth_token")
def token_deleted(sender, instance, **kwargs):
    #oauth.update_token(instance)
    #cache.set(userid=instance.user.id, category='tokens', key=instance.name, value=instance)
    cache.delete(userid=instance.user.id, category=instance.name)
    cache.delete(userid=instance.user.id, category='tokens', key=instance.name)
    print(cache._cache)
