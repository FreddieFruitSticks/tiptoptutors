# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0002_auto_20151223_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='lessons_bought',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='pupil',
            field=models.ForeignKey(to='pupil.Pupil', null=True),
        ),
        migrations.AlterField(
            model_name='pupiltutormatch',
            name='tutor',
            field=models.ForeignKey(to='tutor.Tutor', null=True),
        ),
    ]
