# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20151227_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ECAxis_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ECAxis_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ECAxis_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ICAxis_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ICAxis_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='ICAxis_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MainAxis_X',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MainAxis_Y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='MainAxis_Z',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixpair',
            name='CrossingAngle',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelixtriplet',
            name='Phi',
            field=models.FloatField(null=True),
        ),
    ]
