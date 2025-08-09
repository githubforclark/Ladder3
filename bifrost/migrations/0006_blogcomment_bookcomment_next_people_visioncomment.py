# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bifrost', '0005_auto_20230603_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('BlogID', models.IntegerField()),
                ('UserName', models.CharField(max_length=30)),
                ('CommentBody', models.TextField()),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
            options={
                'db_table': 'BlogComment',
            },
        ),
        migrations.CreateModel(
            name='BookComment',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('BookID', models.IntegerField()),
                ('UserName', models.CharField(max_length=30)),
                ('CommentBody', models.TextField()),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
            options={
                'db_table': 'BookComment',
            },
        ),
        migrations.CreateModel(
            name='Next_People',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('MailAddr', models.EmailField(max_length=254)),
                ('Name', models.CharField(max_length=30)),
                ('Keys', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'db_table': 'Next_People',
            },
        ),
        migrations.CreateModel(
            name='VisionComment',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('VisionID', models.IntegerField()),
                ('UserName', models.CharField(max_length=30)),
                ('CommentBody', models.TextField()),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
            options={
                'db_table': 'VisionComment',
            },
        ),
    ]
