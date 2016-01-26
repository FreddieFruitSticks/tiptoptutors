# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20160123_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingpayment',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='PendingPayment',
        ),
    ]
