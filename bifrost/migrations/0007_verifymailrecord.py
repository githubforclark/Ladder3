# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bifrost', '0006_blogcomment_bookcomment_next_people_visioncomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyMailRecord',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('MailAddr', models.EmailField(max_length=254)),
                ('Code', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
            options={
                'db_table': 'VerifyMailRecord',
            },
        ),
    ]
