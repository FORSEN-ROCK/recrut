# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemaparsing',
            name='context',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='schemaparsing',
            unique_together=set([('domainName', 'context', 'target')]),
        ),
    ]
