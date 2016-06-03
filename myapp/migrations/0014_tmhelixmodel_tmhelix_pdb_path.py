# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20151221_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixmodel',
            name='TMHelix_pdb_path',
            field=models.CharField(default='s', max_length=200),
            preserve_default=False,
        ),
    ]
