import os
from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
from .modules.encryption import encrypt_message, decrypt_message
User = get_user_model()
key = os.getenv("SECRET_KEY")

class Event(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    application = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    severity = models.IntegerField()
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.application + " - " + str(self.severity) + " - " + self.value 

class OauthProvider(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    credentials = models.TextField()
    defaultScope = models.TextField()
    redirectUrl = models.TextField()
    flow = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #if not self.id:
            # Object is a new instance
            
        self.credentials = encrypt_message(self.credentials, key)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.id

class Meterstand(models.Model):
    kwh_180 = models.IntegerField()
    kwh_181 = models.IntegerField()
    kwh_182 = models.IntegerField()
    kwh_280 = models.IntegerField()
    kwh_281 = models.IntegerField()
    kwh_281 = models.IntegerField()
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + str(self.datetime)
    