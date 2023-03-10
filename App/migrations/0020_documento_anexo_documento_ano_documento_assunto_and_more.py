# Generated by Django 4.1.6 on 2023-02-15 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0019_remove_documento_anexo_remove_documento_criadopor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='anexo',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Anexo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='ano',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Ano'),
        ),
        migrations.AddField(
            model_name='documento',
            name='assunto',
            field=models.TextField(blank=True, max_length=15, null=True, verbose_name='Assunto'),
        ),
        migrations.AddField(
            model_name='documento',
            name='criadopor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='datainicial',
            field=models.DateTimeField(blank=True, max_length=15, null=True, verbose_name='Data Inicial'),
        ),
        migrations.AddField(
            model_name='documento',
            name='nome',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='Nome'),
        ),
        migrations.AddField(
            model_name='documento',
            name='numeracao',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Numeração'),
        ),
        migrations.AddField(
            model_name='documento',
            name='prefeitura',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.prefeitura', verbose_name='Prefeitura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='secretaria',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='App.secretaria', verbose_name='Secretária'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='setor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='App.setor', verbose_name='Setor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo',
            field=models.DateField(blank=True, max_length=9, null=True, verbose_name='Tipo'),
        ),
    ]
