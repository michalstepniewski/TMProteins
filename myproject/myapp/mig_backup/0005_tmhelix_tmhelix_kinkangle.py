# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20151207_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_KinkAngle',
            field=models.FloatField(null=True),
        ),
    ]
