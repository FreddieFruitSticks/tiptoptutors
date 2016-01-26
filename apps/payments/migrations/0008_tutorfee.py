# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20160126_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_category', models.CharField(unique=True, max_length=20)),
                ('rate', models.IntegerField()),
            ],
        ),
    ]
