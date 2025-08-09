# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bifrost', '0003_blogs_blog_imglink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('book_title', models.CharField(max_length=30)),
                ('book_describe', models.CharField(max_length=256)),
                ('book_imglink', models.CharField(max_length=256)),
                ('book_content', models.TextField()),
                ('book_status', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'db_table': 'Books',
            },
        ),
        migrations.CreateModel(
            name='Visions',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('vision_title', models.CharField(max_length=30)),
                ('vision_describe', models.CharField(max_length=256)),
                ('vision_imglink', models.CharField(max_length=256)),
                ('vision_content', models.TextField()),
                ('vision_status', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'db_table': 'Visions',
            },
        ),
    ]
