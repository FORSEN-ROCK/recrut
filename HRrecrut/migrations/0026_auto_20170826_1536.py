# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 12:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0025_auto_20170826_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchobject',
            old_name='row_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='searchobject',
            name='domainName',
        ),
    ]