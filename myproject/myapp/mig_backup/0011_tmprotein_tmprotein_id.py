# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20151216_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmprotein',
            name='TMProtein_ID',
            field=models.CharField(default='P_ID', max_length=200),
            preserve_default=False,
        ),
    ]
