from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    #username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
