# Generated by Django 5.0.4 on 2024-06-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crur', '0017_alter_register_response_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='auth',
            field=models.BooleanField(default=False),
        ),
    ]
