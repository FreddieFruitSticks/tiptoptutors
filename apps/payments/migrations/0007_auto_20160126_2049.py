# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20160124_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressreport',
            name='lesson',
            field=models.OneToOneField(null=True, blank=True, to='payments.LessonRecord'),
        ),
    ]
