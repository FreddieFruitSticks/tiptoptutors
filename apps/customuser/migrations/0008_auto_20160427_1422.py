# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
# import pdb; pdb.set_trace()

from django.db import models, migrations


def create_user_for_each_tutor(apps, schema_editor):
    tutors = apps.get_model("tutor", "Tutor")
    users = apps.get_model("customuser", "CustomAuthUser")
    for tutor in tutors.objects.all():
        try:
            user = users.objects.get(email=tutor.email)
        except users.DoesNotExist:
            user = None

        if user is None:
            user = users.objects.create(first_name=tutor.name, last_name=tutor.surname,
                                        email=tutor.email, password=tutor.name)
            user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('customuser', '0007_auto_20160325_1547'),
    ]

    operations = [
        migrations.RunPython(create_user_for_each_tutor)
    ]
