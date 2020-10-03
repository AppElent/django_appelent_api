from django.db import models
from ..modules.encryption import decrypt_message, encrypt_message
import os
key = os.getenv("SECRET_KEY")

class OauthProvider(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    client_id = models.TextField()
    client_secret = models.TextField()
    access_token_url = models.TextField()
    access_token_params = models.TextField(null=True, blank=True)
    authorize_url = models.TextField(null=True, blank=True)
    authorize_params = models.TextField(null=True, blank=True)
    api_base_url = models.TextField(null=True, blank=True)
    client_kwargs = models.TextField(null=True, blank=True)
    defaultScope = models.TextField(null=True, blank=True)
    redirectUrl = models.TextField(null=True, blank=True)
    flow = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def client_secret_decrypted(self):
        # decrypt self.pin and return
        return decrypt_message(self.client_secret, key)

    def save(self, *args, **kwargs):
        #if not self.id:
            # Object is a new instance
            
        self.client_secret = encrypt_message(self.client_secret, key)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name