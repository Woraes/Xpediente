# Generated by Django 4.1.6 on 2023-02-20 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0033_documento_date_envio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='date_envio',
            new_name='data_envio',
        ),
    ]
