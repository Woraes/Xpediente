# Generated by Django 4.1.6 on 2023-02-13 00:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_setor'),
    ]

    operations = [
        migrations.AddField(
            model_name='setor',
            name='telefone',
            field=models.CharField(max_length=17, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Telefone'),
        ),
    ]
