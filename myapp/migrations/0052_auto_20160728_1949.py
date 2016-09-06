# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-28 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0051_auto_20160728_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='TMHelixModel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.TMHelixModel'),
        ),
        migrations.AddField(
            model_name='point',
            name='X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='Z',
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
