# Generated by Django 5.0.4 on 2024-05-06 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crur', '0007_settings_alter_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 6, 19, 58, 24, 907123), null=True),
        ),
    ]