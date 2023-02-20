# Generated by Django 4.1.6 on 2023-02-20 22:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0034_rename_date_envio_documento_data_envio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrada', models.DateTimeField(default=datetime.timezone)),
                ('data_saida', models.DateTimeField(blank=True, null=True)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.documento')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.setor')),
            ],
        ),
    ]
