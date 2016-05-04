# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pdb; pdb.set_trace()

from django.db import migrations
from customuser.forms import CustomUserCreationForm


def create_user_for_each_tutor(apps, schema_editor):
    tutors = apps.get_model("tutor", "Tutor")
    users = apps.get_model("customuser", "CustomAuthUser")
    for tutor in tutors.objects.all():
        try:
            user = users.objects.get(email=tutor.email)
        except users.DoesNotExist:
            user = None

        if user is None:
            data = {'email': tutor.email, 'first_name': tutor.name, 'last_name': tutor.surname,
                    'password1': tutor.name + '$123', 'password2': tutor.name + '$123'}
            user = CustomUserCreationForm(data)
            user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('customuser', '0007_auto_20160325_1547'),
    ]

    operations = [
        migrations.RunPython(create_user_for_each_tutor)
    ]
