# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0005_auto_20151226_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupiltutormatch',
            name='lessons_remaining',
            field=models.IntegerField(verbose_name=b'lessons remaining', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='last_bought_updated',
            field=models.DateField(db_index=True, null=True, verbose_name=b'bought updated', blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='last_taught_updated',
            field=models.DateField(db_index=True, null=True, verbose_name=b'taught updated', blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_bought',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_taught',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
