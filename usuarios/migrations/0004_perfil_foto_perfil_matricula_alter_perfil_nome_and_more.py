# Generated by Django 4.1.6 on 2023-02-16 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0003_rename_usuario_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='foto',
            field=models.ImageField(default=1, upload_to='userfoto/', verbose_name='peril'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='perfil',
            name='matricula',
            field=models.CharField(max_length=20, null=True, verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nome',
            field=models.CharField(max_length=55, null=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]