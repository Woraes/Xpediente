# Generated by Django 4.1.6 on 2023-02-21 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0035_historico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='data_entrada',
            field=models.DateTimeField(),
        ),
    ]
