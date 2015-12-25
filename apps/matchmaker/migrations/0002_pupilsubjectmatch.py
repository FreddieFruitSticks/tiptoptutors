# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PupilSubjectMatch',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'pupil_pupil_subject',
                'managed': False,
            },
        ),
    ]
