# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-11 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0070_auto_20171211_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='search_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HRrecrut.SearchCard'),
        ),
    ]