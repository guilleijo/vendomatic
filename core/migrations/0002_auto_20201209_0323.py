# Generated by Django 3.1.4 on 2020-12-09 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'Inventory'},
        ),
        migrations.AddField(
            model_name='inventory',
            name='machine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='core.machine'),
            preserve_default=False,
        ),
    ]
