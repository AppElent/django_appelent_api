from django.db import models
from django.contrib.auth import get_user_model
from ..fields import EncryptedText, EncryptedTextField

class TestModel(models.Model):
    column1 = EncryptedTextField(decrypt_on_get=True)
