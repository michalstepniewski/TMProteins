# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import myproject.myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_tmhelixmodel_tmhelix_pdb_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMHelixPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='tmprotein',
            name='path',
            field=models.CharField(max_length=200, verbose_name=myproject.myapp.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='tmprotein',
            name='tmproteinfile',
            field=models.FileField(upload_to=myproject.myapp.models.get_upload_path),
        ),
        migrations.AddField(
            model_name='tmhelixmodel',
            name='TMHelixPair',
            field=models.ForeignKey(to='myapp.TMHelixPair', null=True),
        ),
    ]
