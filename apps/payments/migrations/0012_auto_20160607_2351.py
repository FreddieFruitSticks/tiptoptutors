# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20160607_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 7, 23, 51, 47, 889831), verbose_name=b'date/time'),
        ),
    ]
