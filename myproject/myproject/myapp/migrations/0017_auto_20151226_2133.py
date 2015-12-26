# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_tmhelixpair_tmprotein'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tmhelixmodel',
            name='TMHelixPair',
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='TMHelixPair',
            field=models.ManyToManyField(to='myapp.TMHelixPair'),
        ),
    ]
