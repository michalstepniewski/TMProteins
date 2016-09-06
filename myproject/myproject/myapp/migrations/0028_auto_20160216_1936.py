# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_atom_atom_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tmprotein',
            old_name='Atoms',
            new_name='atoms',
        ),
    ]
