# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_auto_20151223_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='status',
            field=models.CharField(default=b'Pending', max_length=10, choices=[(b'Accepted', b'Accepted'), (b'Declined', b'Declined'), (b'Pending', b'Pending')]),
        ),
    ]
