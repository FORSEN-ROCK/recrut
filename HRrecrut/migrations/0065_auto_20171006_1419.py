# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-06 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0064_delete_searchextension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablecolumnhead',
            name='displayName',
            field=models.CharField(max_length=40, verbose_name='Отображаемое название'),
        ),
        migrations.AlterField(
            model_name='tablecolumnhead',
            name='fieldName',
            field=models.CharField(max_length=40, null=True, verbose_name='Поле'),
        ),
        migrations.AlterField(
            model_name='tablecolumnhead',
            name='tableName',
            field=models.CharField(max_length=40, verbose_name='Имя таблицы'),
        ),
    ]