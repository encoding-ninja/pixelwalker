# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 20:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0004_auto_20170927_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='assessment',
        ),
        migrations.RemoveField(
            model_name='result',
            name='date',
        ),
        migrations.RemoveField(
            model_name='result',
            name='encoding_provider',
        ),
        migrations.RemoveField(
            model_name='result',
            name='media',
        ),
        migrations.RemoveField(
            model_name='result',
            name='metric',
        ),
    ]