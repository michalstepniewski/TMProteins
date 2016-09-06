# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-29 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0054_auto_20160729_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixtriplet',
            name='PDBFileName',
            field=models.CharField(max_length=200, null=True),
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
