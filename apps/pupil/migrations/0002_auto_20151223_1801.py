# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupiltutormatch',
            name='lessons_bought',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pupil',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
