# Generated by Django 3.1.2 on 2020-10-04 10:20

import api.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201004_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthprovider',
            name='client_secret',
            field=api.fields.EncryptedTextField(),
        ),
    ]
