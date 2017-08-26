# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRrecrut', '0012_auto_20170820_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='credentials',
            name='password',
        ),
        migrations.RemoveField(
            model_name='credentials',
            name='username',
        ),
        migrations.AddField(
            model_name='credentialsdata',
            name='credentials',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRrecrut.Credentials'),
        ),
        migrations.AlterUniqueTogether(
            name='credentialsdata',
            unique_together=set([('name', 'credentials')]),
        ),
    ]