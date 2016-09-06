# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_tmhelix_tmhelix_overhang'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_AASEQ',
            field=models.CharField(default=datetime.datetime(2015, 12, 15, 21, 15, 42, 792279, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
