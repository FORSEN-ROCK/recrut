# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0003_searchextension_par_row_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchextension',
            old_name='par_row_id',
            new_name='par_row',
        ),
    ]
