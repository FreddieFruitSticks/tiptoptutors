# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_auto_20160102_0213'),
        ('pupil', '0009_auto_20151227_2105'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name=b'date/time')),
                ('amount', models.IntegerField(verbose_name=b'amount')),
                ('pupiltutormatch', models.ForeignKey(to='pupil.PupilTutorMatch')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_paid', models.IntegerField(verbose_name=b'amount paid')),
                ('tutor', models.ForeignKey(to='tutor.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_owing', models.IntegerField(null=True, verbose_name=b'amount owing', blank=True)),
                ('tutor', models.ForeignKey(to='tutor.Tutor', unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='allpayments',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='lessonrecords',
            name='pupiltutormatch',
        ),
        migrations.RemoveField(
            model_name='paymentsduemonthly',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='AllPayments',
        ),
        migrations.DeleteModel(
            name='LessonRecords',
        ),
        migrations.DeleteModel(
            name='PaymentsDueMonthly',
        ),
    ]
