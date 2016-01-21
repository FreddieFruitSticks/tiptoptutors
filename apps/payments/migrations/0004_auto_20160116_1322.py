# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_auto_20160102_0213'),
        ('option', '0001_initial'),
        ('pupil', '0009_auto_20151227_2105'),
        ('payments', '0003_progressreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonrecord',
            name='pupiltutormatch',
        ),
        migrations.RemoveField(
            model_name='progressreport',
            name='homework_given',
        ),
        migrations.AddField(
            model_name='lessonrecord',
            name='paid_status',
            field=models.BooleanField(default=False, verbose_name=b'Paid'),
        ),
        migrations.AddField(
            model_name='lessonrecord',
            name='payment_record',
            field=models.ForeignKey(blank=True, to='payments.PaymentRecord', null=True),
        ),
        migrations.AddField(
            model_name='lessonrecord',
            name='pupil',
            field=models.ForeignKey(to='pupil.Pupil', null=True),
        ),
        migrations.AddField(
            model_name='lessonrecord',
            name='subject',
            field=models.ForeignKey(to='option.AvailableTutorSubject', null=True),
        ),
        migrations.AddField(
            model_name='lessonrecord',
            name='tutor',
            field=models.ForeignKey(to='tutor.Tutor', null=True),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='progressreport',
            name='lesson',
            field=models.OneToOneField(null=True, to='payments.LessonRecord'),
        ),
        migrations.AlterField(
            model_name='lessonrecord',
            name='amount',
            field=models.IntegerField(null=True, verbose_name=b'amount'),
        ),
        migrations.AlterField(
            model_name='pendingpayment',
            name='tutor',
            field=models.OneToOneField(to='tutor.Tutor'),
        ),
        migrations.AlterField(
            model_name='progressreport',
            name='homework_status',
            field=models.CharField(max_length=20, verbose_name=b'Homework completed?', choices=[(b'Complete', b'Complete'), (b'Partially Complete', b'Partially Complete'), (b'Not Complete', b'Not Complete'), (b'First Lesson', b'First Lesson')]),
        ),
    ]
