# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20160116_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrecord',
            name='amount_paid',
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='amount',
            field=models.IntegerField(null=True, verbose_name=b'amount'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
