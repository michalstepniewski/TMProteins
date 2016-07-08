# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_auto_20160213_0726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atom',
            old_name='Content',
            new_name='Text',
        ),
    ]
