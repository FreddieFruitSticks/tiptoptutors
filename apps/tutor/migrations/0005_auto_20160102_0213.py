# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0004_tutor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='user',
            field=models.OneToOneField(null=True, default=None, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
