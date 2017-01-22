# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0012_auto_20160526_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupil',
            name='guardian_name',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'Guardian name'),
        ),
    ]
