# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_auto_20160721_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmhelixpair',
            name='ContactAtoms',
            field=models.CharField(max_length=20000, null=True),
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
