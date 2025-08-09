# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bifrost', '0004_books_visions'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='book_jumbo_imglink',
            field=models.CharField(max_length=256, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='books',
            name='book_jumbo_space',
            field=models.CharField(max_length=256, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='books',
            name='book_jumbo_title',
            field=models.CharField(max_length=30, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visions',
            name='vision_jumbo_imglink',
            field=models.CharField(max_length=256, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visions',
            name='vision_jumbo_space',
            field=models.CharField(max_length=256, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visions',
            name='vision_jumbo_title',
            field=models.CharField(max_length=30, default=2),
            preserve_default=False,
        ),
    ]
