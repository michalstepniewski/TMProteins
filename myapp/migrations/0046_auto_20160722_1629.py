# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_auto_20160722_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixtriplet',
            name='CrossingAngle1_3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixtriplet',
            name='CrossingAngle2_3',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='xlsfile',
            name='path',
            field=models.CharField(max_length=200, verbose_name=myapp.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='xlsfile',
            name='xlsfile',
            field=models.FileField(upload_to=myapp.models.get_upload_path),
        ),
    ]