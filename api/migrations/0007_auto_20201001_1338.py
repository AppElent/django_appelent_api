# Generated by Django 3.1.1 on 2020-10-01 11:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201001_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauth2token',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oauth2token',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
