# Generated by Django 4.1.6 on 2023-02-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_alter_colaborador_estadocivil_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='email',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='matricula',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='nome',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='phone',
            field=models.CharField(max_length=16, null=True, unique=True, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='status',
            field=models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], max_length=10, null=True, verbose_name='Status'),
        ),
    ]
