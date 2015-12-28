# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0008_auto_20151227_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupil',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'Pupil name'),
        ),
    ]
