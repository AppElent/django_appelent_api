from django.dispatch import receiver
from authlib.integrations.django_client import token_update
from .models import OAuth2Token

@receiver(token_update)
def update_token(
    name, token, refresh_token=None, access_token=None, **kwargs
):
    OAuth2Token.objects.update_token(name, token, refresh_token, access_token)