# Generated by Django 4.1.6 on 2023-02-22 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0040_documento_data_criacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='data_criacao',
        ),
    ]