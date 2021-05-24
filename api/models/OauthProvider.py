from django.db import models
from ..modules.encryption import decrypt_message, encrypt_message
from ..modules.encrypted_fields import EncryptedTextField
import os
key = os.getenv("SECRET_KEY")

class OauthProvider(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    client_id = models.TextField()
    client_secret = EncryptedTextField(decrypt_on_get=True)
    access_token_url = models.TextField()
    access_token_params = models.TextField(null=True, blank=True)
    authorize_url = models.TextField(null=True, blank=True)
    authorize_params = models.TextField(null=True, blank=True)
    refresh_token_url = models.TextField(null=True, blank=True)
    refresh_token_params = models.TextField(null=True, blank=True)
    api_base_url = models.TextField(null=True, blank=True)
    client_kwargs = models.TextField(null=True, blank=True)
    default_scope = models.TextField(null=True, blank=True)
    redirect_uri = models.TextField(null=True, blank=True)
    flow = models.TextField(null=True, blank=True, choices=[('password', 'password'), ('authorization_code', 'authorization_code')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name