# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20160208_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmprotein',
            name='Atoms',
            field=models.TextField(default=b'fejslik', null=True),
        ),
    ]
