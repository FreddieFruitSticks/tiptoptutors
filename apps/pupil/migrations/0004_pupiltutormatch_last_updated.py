# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0003_auto_20151225_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupiltutormatch',
            name='last_updated',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
    ]
