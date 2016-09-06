# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20151107_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_ID',
            field=models.CharField(default=datetime.datetime(2015, 11, 7, 19, 45, 49, 874088, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_Tilt',
            field=models.FloatField(null=True),
        ),
    ]
