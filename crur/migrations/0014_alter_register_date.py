# Generated by Django 5.0.4 on 2024-05-15 13:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crur', '0013_alter_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Data'),
        ),
    ]
