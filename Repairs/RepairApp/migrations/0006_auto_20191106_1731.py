# Generated by Django 2.2.1 on 2019-11-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RepairApp', '0005_auto_20191105_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='nivel',
        ),
        migrations.AddField(
            model_name='myuser',
            name='admin',
            field=models.BooleanField(default=False, verbose_name='administrador'),
        ),
    ]