# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 21:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0019_structure_processed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structure',
            name='Processed',
        ),
    ]
