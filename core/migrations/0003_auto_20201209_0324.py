# Generated by Django 3.1.4 on 2020-12-09 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201209_0323'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('machine', 'beverage_type')},
        ),
    ]