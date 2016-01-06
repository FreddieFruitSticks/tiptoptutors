# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20160104_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('homework_status', models.CharField(max_length=20, choices=[(b'Complete', b'Complete'), (b'Partially Complete', b'Partially Complete'), (b'Not Complete', b'Not Complete'), (b'First Lesson', b'First Lesson')])),
                ('homework_given', models.BooleanField(help_text=b'select if homework was given')),
                ('homework_summary', models.TextField(help_text=b"give a week's worth of HW (160 Characters)", max_length=160, verbose_name=b'Summary of homework given')),
                ('student_summary', models.TextField(help_text=b'Indicate how student is coping with work, what needs improving, tutor advice, etc', max_length=200, verbose_name=b'Summary of student progress')),
            ],
        ),
    ]
