# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0021_remove_schemaparsing_domainname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schemaparsing',
            old_name='row_id',
            new_name='id',
        ),
    ]