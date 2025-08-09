# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(max_length=30)),
                ('blog_describe', models.CharField(max_length=256)),
                ('blog_content', models.TextField()),
                ('blog_status', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'db_table': 'Blogs',
            },
        ),
    ]
