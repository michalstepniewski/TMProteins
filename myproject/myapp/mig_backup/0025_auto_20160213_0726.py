# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_tmprotein_atoms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Content', models.CharField(max_length=200)),
                ('TMHelixModel', models.ForeignKey(to='myapp.TMHelixModel', null=True)),
                ('TMProtein', models.ForeignKey(to='myapp.TMProtein', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Residue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='atomline',
            name='TMHelixModel',
        ),
        migrations.RemoveField(
            model_name='atomline',
            name='TMProtein',
        ),
        migrations.DeleteModel(
            name='AtomLineManager',
        ),
        migrations.DeleteModel(
            name='AtomLine',
        ),
    ]
