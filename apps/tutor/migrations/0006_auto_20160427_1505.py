# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model

from django.db import models, migrations
import settings


def set_user_on_tutor(apps, schema_editor):
    tutors = apps.get_model("tutor", "Tutor")
    users = apps.get_model("customuser", "CustomAuthUser")

    for tutor in tutors.objects.all():
        try:
            user = users.objects.get(email=tutor.email)
        except get_user_model().DoesNotExist:
            user = None

        tutor.user = user
        tutor.save()


class Migration(migrations.Migration):
    dependencies = [
        ('tutor', '0005_auto_20160102_0213'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(set_user_on_tutor)
    ]
