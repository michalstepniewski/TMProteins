# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0043_auto_20160722_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tmhelixpair',
            old_name='TMHeliX_IDs',
            new_name='TMHelix_IDs',
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