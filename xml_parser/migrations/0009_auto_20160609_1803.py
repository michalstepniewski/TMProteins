# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0008_auto_20160609_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliography',
            name='doi',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
