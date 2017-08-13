# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='list_of_value',
            fields=[
                ('row_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('lang_id', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchemaParsing',
            fields=[
                ('row_id', models.AutoField(primary_key=True, serialize=False)),
                ('domainName', models.CharField(max_length=100)),
                ('target', models.CharField(max_length=100)),
                ('tagName', models.CharField(max_length=40)),
                ('attributeName', models.CharField(max_length=100)),
                ('attributeValue', models.CharField(max_length=200)),
                ('expression', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchExtension',
            fields=[
                ('row_id', models.AutoField(primary_key=True, serialize=False)),
                ('baseSequence', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SearchObject',
            fields=[
                ('row_id', models.AutoField(primary_key=True, serialize=False)),
                ('domainName', models.CharField(max_length=100)),
                ('SearchMode', models.CharField(max_length=50)),
                ('age', models.BooleanField(default=False)),
                ('gender', models.BooleanField(default=False)),
                ('pay', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=500)),
                ('parametrs', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='searchobject',
            unique_together=set([('domainName', 'SearchMode', 'age', 'gender', 'pay', 'parametrs')]),
        ),
        migrations.AlterUniqueTogether(
            name='searchextension',
            unique_together=set([('row_id', 'baseSequence')]),
        ),
        migrations.AlterUniqueTogether(
            name='schemaparsing',
            unique_together=set([('domainName', 'target')]),
        ),
        migrations.AlterUniqueTogether(
            name='list_of_value',
            unique_together=set([('type', 'name')]),
        ),
    ]
