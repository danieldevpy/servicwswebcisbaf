# Generated by Django 5.0.4 on 2024-06-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crur', '0016_register_response_attachments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='response_attachments',
            field=models.ManyToManyField(blank=True, null=True, related_name='register_response_attachments', to='crur.archive'),
        ),
    ]
