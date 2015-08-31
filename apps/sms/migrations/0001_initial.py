# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile_number', models.CharField(max_length=12)),
                ('delivery_status', models.TextField(default=b'unknown')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message_id', models.CharField(db_index=True, max_length=32, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'SMS',
                'verbose_name_plural': 'SMSes',
            },
            bases=(models.Model,),
        ),
    ]
