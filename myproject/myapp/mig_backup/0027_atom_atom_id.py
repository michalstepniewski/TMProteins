# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_auto_20160213_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='Atom_ID',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
