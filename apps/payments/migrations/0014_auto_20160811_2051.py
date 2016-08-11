# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_auto_20160607_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='datetime',
            field=models.DateTimeField(verbose_name=b'date/time'),
        ),
    ]
