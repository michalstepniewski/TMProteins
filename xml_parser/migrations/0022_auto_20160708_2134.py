# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0021_structure_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='Processed',
            field=models.NullBooleanField(default=False),
        ),
    ]
