# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20151221_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmprotein',
            name='path',
            field=models.CharField(default='s', max_length=200, verbose_name=b'uploads/%Y/%m/%d/%H/%M'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tmprotein',
            name='tmproteinfile',
            field=models.FileField(upload_to=b'uploads/%Y/%m/%d/%H/%M'),
        ),
    ]
