# Generated by Django 3.1.4 on 2020-12-22 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_oauth2state_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauth2token',
            name='expires_at',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
