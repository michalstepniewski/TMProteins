# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0005_auto_20160609_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliography',
            name='notes',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]