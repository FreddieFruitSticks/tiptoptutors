# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
        ('option', '0001_initial'),
        ('pupil', '0001_initial'),
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForTutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'active', max_length=8, choices=[(b'active', b'Active'), (b'inactive', b'Inactive')])),
                ('code', models.CharField(unique=True, max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ForeignKey(to='option.AvailableTutorSubject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestSMS',
            fields=[
                ('sms_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='sms.SMS')),
                ('response_text', models.CharField(max_length=256, null=True, blank=True)),
                ('response_timestamp', models.DateTimeField(null=True, blank=True)),
                ('requests', models.ManyToManyField(to='matchmaker.RequestForTutor')),
            ],
            options={
                'verbose_name': 'Request SMS',
                'verbose_name_plural': 'Request SMSes',
            },
            bases=('sms.sms',),
        ),
        migrations.CreateModel(
            name='PupilProxy',
            fields=[
            ],
            options={
                'ordering': ('-created_at', 'surname', 'name'),
                'verbose_name': 'pupil',
                'proxy': True,
                'verbose_name_plural': 'pupils',
            },
            bases=('pupil.pupil',),
        ),
        migrations.AddField(
            model_name='requestfortutor',
            name='pupil',
            field=models.ForeignKey(to='matchmaker.PupilProxy'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TutorProxy',
            fields=[
            ],
            options={
                'verbose_name': 'available tutor',
                'proxy': True,
                'verbose_name_plural': 'available tutors',
            },
            bases=('tutor.tutor',),
        ),
        migrations.AddField(
            model_name='requestsms',
            name='tutor',
            field=models.ForeignKey(to='matchmaker.TutorProxy'),
            preserve_default=True,
        ),
    ]
