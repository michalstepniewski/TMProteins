# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xml_parser', '0024_databasemodel_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('parameters', models.CharField(max_length=2000, null=True)),
                ('DatabaseModel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xml_parser.DatabaseModel')),
            ],
        ),
    ]
