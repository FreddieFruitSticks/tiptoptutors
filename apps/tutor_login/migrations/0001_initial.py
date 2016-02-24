# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sites.models import Site

from django.db import models, migrations


def add_livesite_url(apps, schema_editor):
    livesite = Site(domain='www.tiptoptutors.co.za', name='www.tiptoptutors.co.za')
    livesite.save()


def remove_livesite_url(apps, schema_editor):
    Sites = apps.get_model("django.contrib.sites", "Site")
    Sites.objects.get(name='www.tiptoptutor.co.za').delete()


class Migration(migrations.Migration):
    initial = True
    dependencies = [
    #     ('django.contrib.sites', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_livesite_url),
    ]
