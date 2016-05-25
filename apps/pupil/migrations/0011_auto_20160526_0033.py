# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0010_pupilpin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_bought',
            field=models.DecimalField(default=0, null=True, max_digits=5, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_taught',
            field=models.DecimalField(default=0, null=True, max_digits=5, decimal_places=1, blank=True),
        ),
    ]
