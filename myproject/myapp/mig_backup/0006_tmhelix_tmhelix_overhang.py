# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_tmhelix_tmhelix_kinkangle'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='TMHelix_Overhang',
            field=models.FloatField(null=True),
        ),
    ]
