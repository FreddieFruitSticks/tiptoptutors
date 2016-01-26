# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0009_auto_20151227_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='PupilPin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(max_length=4)),
                ('pupil', models.ForeignKey(to='pupil.Pupil')),
            ],
        ),
    ]
