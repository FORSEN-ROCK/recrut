# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0026_auto_20170826_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchobject',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
