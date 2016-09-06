# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20151227_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_EC_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_EC_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_EC_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_IC_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_IC_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_IC_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_MM_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_MM_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MC_MM_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixpair',
            name='CrossingAngleEC',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixpair',
            name='CrossingAngleIC',
            field=models.FloatField(null=True),
        ),
    ]
