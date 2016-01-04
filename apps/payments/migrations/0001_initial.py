# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_auto_20160102_0213'),
        ('pupil', '0009_auto_20151227_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllPayments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_paid', models.IntegerField(verbose_name=b'amount paid')),
                ('tutor', models.ForeignKey(to='tutor.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='LessonRecords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name=b'date/time')),
                ('amount', models.IntegerField(verbose_name=b'amount')),
                ('pupiltutormatch', models.ForeignKey(to='pupil.PupilTutorMatch')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentsDueMonthly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_owing', models.IntegerField(null=True, verbose_name=b'amount owing', blank=True)),
                ('tutor', models.ForeignKey(to='tutor.Tutor', unique=True)),
            ],
        ),
    ]
