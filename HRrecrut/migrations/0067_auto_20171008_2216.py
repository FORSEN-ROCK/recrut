# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-08 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0066_auto_20171006_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='inactive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='resume',
            name='gender',
            field=models.CharField(choices=[('all', 'Неважно'), ('female', 'Женский'), ('man', 'Мужской')], max_length=7, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='searchcard',
            name='gender',
            field=models.CharField(choices=[('all', 'Неважно'), ('female', 'Женский'), ('man', 'Мужской')], max_length=7, verbose_name='Пол'),
        ),
    ]
