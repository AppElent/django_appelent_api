# Generated by Django 3.1.4 on 2020-12-22 09:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201222_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauth2state',
            name='name',
            field=models.CharField(default='enelogic', max_length=200),
            preserve_default=False,
        ),
    ]
