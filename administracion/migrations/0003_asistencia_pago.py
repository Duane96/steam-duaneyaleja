# Generated by Django 5.0 on 2024-01-22 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_asistencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='pago',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administracion.pago'),
            preserve_default=False,
        ),
    ]
