# Generated by Django 5.0.4 on 2024-05-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='field_extra',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
