# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='Type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
