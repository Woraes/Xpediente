# Generated by Django 4.1.6 on 2023-02-13 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_colaborador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='dataentrada',
            field=models.DateTimeField(max_length=10, null=True, verbose_name='Data de Entrada'),
        ),
    ]