from django.db import models
from django.utils.functional import cached_property
from .modules.encryption import encrypt_message, decrypt_message
import os
key = os.getenv('SECRET_KEY')

class EncryptedText(models.TextField):
    description = "Encrypts a field before saving and decrypts upon retrieval"

    def from_db_value(self, value, expression, connection):
        print('from db value')
        return decrypt_message(value, key)

    def to_python(self, value):
        print('to python')
        try:
            return encrypt_message(value, key)
        except TypeError:
            return value


class EncryptedMixin(object):

    def __init__(self, *args, **kwargs):
        self.decrypt_on_get = kwargs.pop('decrypt_on_get', False) # pop the custom kwarg
        self.key = kwargs.pop('key', key)
        super(EncryptedMixin, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            if self.decrypt_on_get == True:
                value = decrypt_message(value, self.key)
        except:
            pass


        return super(EncryptedMixin, self).to_python(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedMixin, self).get_db_prep_save(value, connection)

        if value is None:
            return value
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return (encrypt_message(str(value), self.key))

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

