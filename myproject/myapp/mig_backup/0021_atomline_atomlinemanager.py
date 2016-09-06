# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20151229_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtomLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Content', models.CharField(max_length=200)),
                ('TMHelixModel', models.ForeignKey(to='myapp.TMHelixModel', null=True)),
                ('TMProtein', models.ForeignKey(to='myapp.TMProtein', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AtomLineManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
