# Generated by Django 4.1.6 on 2023-02-16 05:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0002_alter_usuario_cpf'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usuario',
            new_name='Perfil',
        ),
    ]
