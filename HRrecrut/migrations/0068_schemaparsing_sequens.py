# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-14 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0067_auto_20171008_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemaparsing',
            name='sequens',
            field=models.IntegerField(null=True),
        ),
    ]