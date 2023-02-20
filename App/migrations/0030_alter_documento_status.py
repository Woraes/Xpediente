# Generated by Django 4.1.6 on 2023-02-20 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0029_alter_documento_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='status',
            field=models.CharField(choices=[('registrado', 'Registrado'), ('enviado', 'Enviado'), ('recebido', 'Recebido')], max_length=10, null=True, verbose_name='Status'),
        ),
    ]
