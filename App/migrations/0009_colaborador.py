# Generated by Django 4.1.6 on 2023-02-13 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0008_setor_telefone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60, null=True, verbose_name='Nome')),
                ('nascimento', models.DateField(max_length=9, null=True, verbose_name='Nascimento')),
                ('estadocivil', models.CharField(choices=[('Solteiro', 'Solteiro'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'), ('Viúvo', 'Viúvo')], max_length=15, null=True, verbose_name='Estadocivil')),
                ('matricula', models.CharField(max_length=15, null=True, verbose_name='Matrícula')),
                ('rg', models.CharField(max_length=15, null=True, verbose_name='Rg')),
                ('cpf', models.CharField(max_length=15, null=True, unique=True, verbose_name='CPF')),
                ('pis', models.CharField(max_length=16, null=True, unique=True, verbose_name='PIS')),
                ('cns', models.CharField(max_length=16, null=True, unique=True, verbose_name='Cns')),
                ('ctps', models.CharField(max_length=7, null=True, verbose_name='Ctps número:')),
                ('ctpsserie', models.CharField(max_length=4, null=True, verbose_name='Série')),
                ('ctpsuf', models.CharField(max_length=2, null=True, verbose_name='UF')),
                ('genero', models.CharField(choices=[('MASCULINO', 'MASCULINO'), ('FEMININO', 'FEMININO'), ('NÃO DEFINIDO', 'NÃO DEFINIDO')], max_length=16, null=True, verbose_name='Genero')),
                ('phone', models.CharField(max_length=16, null=True, verbose_name='Celular')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='Colaborador_foto', verbose_name='Foto')),
                ('status', models.CharField(choices=[('ativo', 'ativo'), ('inativo', 'inativo')], max_length=10, null=True, verbose_name='Status')),
                ('dataentrada', models.DateField(max_length=10, null=True, verbose_name='Status')),
                ('cep', models.CharField(max_length=8, null=True, verbose_name='cep')),
                ('logradouro', models.CharField(blank=True, max_length=70, null=True, verbose_name='logradouro')),
                ('complemento', models.CharField(blank=True, max_length=70, null=True, verbose_name='complemento')),
                ('bairro', models.CharField(blank=True, max_length=70, null=True, verbose_name='bairro')),
                ('localidade', models.CharField(blank=True, max_length=70, null=True, verbose_name='localidade')),
                ('uf', models.CharField(blank=True, max_length=10, null=True, verbose_name='uf')),
                ('criadopor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('prefeitura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.prefeitura', verbose_name='Prefeitura')),
                ('secretaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.secretaria', verbose_name='Secretária')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.setor', verbose_name='Setor')),
            ],
        ),
    ]
