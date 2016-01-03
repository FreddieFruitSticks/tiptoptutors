# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0006_auto_20151227_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_remaining',
            field=models.IntegerField(null=True, verbose_name=b'lessons remaining', blank=True),
        ),
    ]