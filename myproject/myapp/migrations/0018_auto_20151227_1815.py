# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_auto_20151226_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMHelixTriplet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TMProtein', models.ForeignKey(to='myapp.TMProtein', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='TMHelixTriplet',
            field=models.ManyToManyField(to='myapp.TMHelixTriplet'),
        ),
    ]
