# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0028_searchobject_domain'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchsequence',
            old_name='row_id',
            new_name='id',
        ),
        migrations.AlterUniqueTogether(
            name='searchsequence',
            unique_together=set([]),
        ),
    ]
