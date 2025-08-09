# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bifrost', '0002_auto_20230531_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='blog_imglink',
            field=models.CharField(max_length=256, default=2),
            preserve_default=False,
        ),
    ]
