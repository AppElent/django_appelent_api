# Generated by Django 3.1.4 on 2020-12-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20201222_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthprovider',
            name='refresh_token_params',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='oauthprovider',
            name='refresh_token_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
