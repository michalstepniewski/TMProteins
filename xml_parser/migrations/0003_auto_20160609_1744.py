# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0002_auto_20160608_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protein',
            name='group',
        ),
        migrations.AddField(
            model_name='bibliography',
            name='structure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.structure'),
        ),
        migrations.AddField(
            model_name='group',
            name='DatabaseModel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.DatabaseModel'),
        ),
        migrations.AddField(
            model_name='protein',
            name='subgroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.subgroup'),
        ),
        migrations.AddField(
            model_name='structure',
            name='protein',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.protein'),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.group'),
        ),
    ]