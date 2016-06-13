# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_auto_20160604_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 7, 23, 37, 37, 775926), verbose_name=b'date/time'),
        ),
    ]
