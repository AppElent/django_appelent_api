# Generated by Django 3.1.2 on 2020-10-10 07:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20201004_1502'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='meterstand',
            unique_together={('datetime', 'user')},
        ),
    ]
