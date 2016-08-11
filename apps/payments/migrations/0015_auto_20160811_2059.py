# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_auto_20160811_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date/time'),
        ),
    ]
