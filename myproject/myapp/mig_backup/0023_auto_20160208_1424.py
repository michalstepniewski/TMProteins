# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_tmhelixmodel_atoms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmhelixmodel',
            name='Atoms',
            field=models.TextField(default=b'fejslik', null=True),
        ),
    ]
