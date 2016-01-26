# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_tutorfee'),
        ('option', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelofstudy',
            name='rate_category',
            field=models.ForeignKey(blank=True, to='payments.TutorFee', null=True),
        ),
    ]
