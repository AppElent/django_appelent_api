from django.db import models
from ..modules.encrypted_fields import EncryptedTextField

class TestModel(models.Model):
    column1 = EncryptedTextField(decrypt_on_get=True)
    encrypted_value = EncryptedTextField(decrypt_on_get=False)
