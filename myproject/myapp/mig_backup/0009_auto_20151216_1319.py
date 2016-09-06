# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_tmhelix_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMProteinManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tmhelix',
            name='Document',
        ),
        migrations.AddField(
            model_name='tmhelix',
            name='TMProtein',
            field=models.ForeignKey(default=1, to='myapp.TMProtein'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tmprotein',
            name='tmproteinfile',
            field=models.FileField(default=1, upload_to=b''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
