# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0007_auto_20151227_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pupiltutormatch',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='pupiltutormatch',
            name='start_date',
        ),
    ]
