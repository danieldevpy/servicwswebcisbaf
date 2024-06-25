# Generated by Django 5.0.4 on 2024-04-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=100, verbose_name='Identificador')),
                ('data_json', models.CharField(max_length=1000, verbose_name='Dados em JSON')),
                ('archives', models.ManyToManyField(to='crur.archive')),
            ],
        ),
    ]