# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0004_pupiltutormatch_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pupiltutormatch',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='pupiltutormatch',
            name='last_bought_updated',
            field=models.DateField(db_index=True, null=True, verbose_name=b'bought_updated', blank=True),
        ),
        migrations.AddField(
            model_name='pupiltutormatch',
            name='last_taught_updated',
            field=models.DateField(db_index=True, null=True, verbose_name=b'taught_updated', blank=True),
        ),
        migrations.AddField(
            model_name='pupiltutormatch',
            name='lessons_taught',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
