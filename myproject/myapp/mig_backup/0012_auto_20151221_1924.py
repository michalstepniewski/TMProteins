# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_tmprotein_tmprotein_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmprotein',
            name='tmproteinfile',
            field=models.FileField(upload_to=models.CharField(max_length=200)),
        ),
    ]
