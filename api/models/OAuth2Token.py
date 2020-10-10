from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from crum import get_current_user
from ..modules.encrypted_fields import EncryptedTextField
User = get_user_model()
import os
key = os.getenv("SECRET_KEY")

class OAuth2TokenManager(models.Manager):
    def update_token(self, name, token, refresh_token=None, access_token=None):
        print('Auto update of token ' + name)
        if refresh_token:
            item = self.get(name=name, refresh_token=refresh_token)
        elif access_token:
            item = self.get(name=name, access_token=access_token)
        else:
            return

        # update old token
        item.update(token)

class OAuth2Token(models.Model):
    objects = OAuth2TokenManager()
    
    name = models.CharField(max_length=40)
    token_type = models.CharField(max_length=40)
    access_token = EncryptedTextField(decrypt_on_get=True)
    refresh_token = models.CharField(max_length=200, blank=True, null=True)
    expires_at = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'user',)

    @property
    def expires_at_string(self):
        if self.expires_at is None:
            return None
        return datetime.fromtimestamp(self.expires_at).strftime("%m/%d/%Y, %H:%M:%S")

    @property
    def expired(self):
        #return self.expires_at < pendulum.now()
        return False

    def update(self, token):
        self.access_token = token["access_token"]
        self.refresh_token = token.get("refresh_token")
        self.expires_at = token["expires_at"]
        self.token_type = token["token_type"]
        self.save()

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )

    def __str__(self):
        expires_string = "" if self.expires_at is None else self.expires_at_string
        return self.name + " - " + self.user.email + " - Expires: " + expires_string