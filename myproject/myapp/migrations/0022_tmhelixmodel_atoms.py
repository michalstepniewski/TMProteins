# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_atomline_atomlinemanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixmodel',
            name='Atoms',
            field=models.TextField(null=True),
        ),
    ]
