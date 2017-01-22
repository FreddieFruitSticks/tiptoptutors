# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaker', '0002_pupilsubjectmatch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pupilproxy',
            options={'ordering': ('-created_at', 'surname', 'name', 'guardian_name'), 'verbose_name': 'pupil', 'verbose_name_plural': 'pupils'},
        ),
    ]
