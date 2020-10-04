from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from cryptography.fernet import Fernet
import os
appkey = settings.FIELD_ENCRYPTION_KEY if hasattr(settings, 'FIELD_ENCRYPTION_KEY') else os.getenv('SECRET_KEY')

def encrypt_message(message, key):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message.decode('utf-8')

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())

    return decrypted_message.decode('utf-8')

class EncryptedMixin(object):

    _ENCRYPTED_PREFIX = 'encrypted_'

    def remove_prefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text  # or whatever

    def __init__(self, *args, **kwargs):
        self.decrypt_on_get = kwargs.pop('decrypt_on_get', False) # pop the custom kwarg
        self.key = kwargs.pop('key', appkey)
        super(EncryptedMixin, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            if self.decrypt_on_get == True:
                value = decrypt_message(self.remove_prefix(value, self._ENCRYPTED_PREFIX), self.key)
        except:
            pass


        return super(EncryptedMixin, self).to_python(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedMixin, self).get_db_prep_save(value, connection)

        if value is None:
            return value
        if value.startswith(self._ENCRYPTED_PREFIX):
            return value
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return (self._ENCRYPTED_PREFIX + encrypt_message(str(value), self.key))

    def get_internal_type(self):
        return "TextField"

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedMixin, self).deconstruct()

        if 'max_length' in kwargs:
            del kwargs['max_length']

        return name, path, args, kwargs


class EncryptedCharField(EncryptedMixin, models.CharField):
    pass


class EncryptedTextField(EncryptedMixin, models.TextField):
    pass


class EncryptedDateField(EncryptedMixin, models.DateField):
    pass


class EncryptedDateTimeField(EncryptedMixin, models.DateTimeField):
    pass


class EncryptedEmailField(EncryptedMixin, models.EmailField):
    pass


class EncryptedBooleanField(EncryptedMixin, models.BooleanField):

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        if value is True:
            value = '1'
        elif value is False:
            value = '0'
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return encrypt_str(str(value)).decode('utf-8')


class EncryptedNullBooleanField(EncryptedMixin, models.NullBooleanField):

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        if value is True:
            value = '1'
        elif value is False:
            value = '0'
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return encrypt_str(str(value)).decode('utf-8')


class EncryptedNumberMixin(EncryptedMixin):
    max_length = 20

    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        range_validators = []
        internal_type = self.__class__.__name__[9:]
        min_value, max_value = django.db.connection.ops.integer_field_range(internal_type)
        if min_value is not None:
            range_validators.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            range_validators.append(validators.MaxValueValidator(max_value))
        return super(EncryptedNumberMixin, self).validators + range_validators


class EncryptedIntegerField(EncryptedNumberMixin, models.IntegerField):
    description = "An IntegerField that is encrypted before " \
                  "inserting into a database using the python cryptography " \
                  "library"
    pass


class EncryptedPositiveIntegerField(EncryptedNumberMixin, models.PositiveIntegerField):
    pass


class EncryptedSmallIntegerField(EncryptedNumberMixin, models.SmallIntegerField):
    pass


class EncryptedPositiveSmallIntegerField(EncryptedNumberMixin, models.PositiveSmallIntegerField):
    pass


class EncryptedBigIntegerField(EncryptedNumberMixin, models.BigIntegerField):
    pass

