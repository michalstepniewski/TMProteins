# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20151216_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMHelixModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TMHelix_ID', models.CharField(max_length=200)),
                ('TMHelix_AASEQ', models.CharField(max_length=200)),
                ('TMHelix_Tilt', models.FloatField(null=True)),
                ('TMHelix_Tilt_EC', models.FloatField(null=True)),
                ('TMHelix_Tilt_IC', models.FloatField(null=True)),
                ('TMHelix_KinkAngle', models.FloatField(null=True)),
                ('TMHelix_Overhang', models.FloatField(null=True)),
                ('TMProtein', models.ForeignKey(to='myapp.TMProtein', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tmhelix',
            name='TMProtein',
        ),
        migrations.DeleteModel(
            name='TMProteinManager',
        ),
        migrations.DeleteModel(
            name='TMHelix',
        ),
    ]
