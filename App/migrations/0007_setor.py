# Generated by Django 4.1.6 on 2023-02-13 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0006_alter_secretaria_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, null=True, verbose_name='Nome do setor')),
                ('status', models.CharField(choices=[('ativo', 'ativo'), ('inativo', 'inativo')], max_length=10, null=True, verbose_name='Status')),
                ('cep', models.CharField(max_length=8, null=True, verbose_name='cep')),
                ('logradouro', models.CharField(blank=True, max_length=70, null=True, verbose_name='logradouro')),
                ('complemento', models.CharField(blank=True, max_length=70, null=True, verbose_name='complemento')),
                ('bairro', models.CharField(blank=True, max_length=70, null=True, verbose_name='bairro')),
                ('localidade', models.CharField(blank=True, max_length=70, null=True, verbose_name='localidade')),
                ('uf', models.CharField(blank=True, max_length=10, null=True, verbose_name='uf')),
                ('criadopor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('prefeitura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.prefeitura', verbose_name='Prefeitura')),
                ('secretaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.secretaria', verbose_name='Secretária')),
            ],
        ),
    ]
