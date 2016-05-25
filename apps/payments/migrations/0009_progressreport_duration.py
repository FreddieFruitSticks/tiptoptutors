# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_tutorfee'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressreport',
            name='duration',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1, choices=[(0.5, b'30min'), (1, b'1 hour'), (1.5, b'1hour30min'), (2, b'2 hours')]),
        ),
    ]
