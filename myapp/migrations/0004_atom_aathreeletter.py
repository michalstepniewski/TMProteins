# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_residue_aathreeletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='AAThreeLetter',
            field=models.CharField(max_length=3, null=True),
        ),
    ]