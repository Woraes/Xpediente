# Generated by Django 4.1.6 on 2023-02-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_alter_secretaria_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretaria',
            name='nome',
            field=models.CharField(max_length=40, null=True, unique=True, verbose_name='Nome da Secretária'),
        ),
    ]