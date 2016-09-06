# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_tmhelix_tmhelix_aaseq'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmhelix',
            name='Document',
            field=models.ForeignKey(default=1, to='myapp.Document'),
            preserve_default=False,
        ),
    ]
