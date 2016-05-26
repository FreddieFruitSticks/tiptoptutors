# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0011_auto_20160526_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_remaining',
            field=models.DecimalField(null=True, verbose_name=b'lessons remaining', max_digits=5, decimal_places=1, blank=True),
        ),
    ]
