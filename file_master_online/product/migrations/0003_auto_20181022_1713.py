# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20180726_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='published_date',
        ),
        migrations.AddField(
            model_name='product',
            name='revision',
            field=models.IntegerField(default=1),
        ),
    ]
