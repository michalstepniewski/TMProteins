# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='file',
            field=models.FileField(upload_to=b'pictures'),
        ),
    ]
