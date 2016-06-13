# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_progressreport_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 4, 17, 43, 21, 775448), verbose_name=b'date/time'),
        ),
    ]
