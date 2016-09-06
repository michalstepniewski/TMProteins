# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20151226_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelixpair',
            name='TMProtein',
            field=models.ForeignKey(to='myapp.TMProtein', null=True),
        ),
    ]
