# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20151107_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_Tilt_EC',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_Tilt_IC',
            field=models.FloatField(null=True),
        ),
    ]
