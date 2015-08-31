# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('option', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'name')),
                ('surname', models.CharField(max_length=20, verbose_name=b'surname')),
                ('gender', models.CharField(max_length=6, verbose_name=b'gender', choices=[(b'male', b'Male'), (b'female', b'Female'), (b'other', b'Other')])),
                ('email', models.EmailField(max_length=75, verbose_name=b'email')),
                ('mobile', models.CharField(max_length=10, verbose_name=b'mobile number')),
                ('transport', models.BooleanField(default=False, help_text=b'Do you have your own transport?', verbose_name=b'Transport')),
                ('id_passport', models.CharField(max_length=20, verbose_name=b'ID/passport number')),
                ('status', models.CharField(default=b'2', max_length=10, choices=[(b'Accepted', b'Accepted'), (b'Declined', b'Declined'), (b'Pending', b'Pending')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('academic', models.ForeignKey(related_name='academic_tutors', blank=True, to='common.Document', help_text=b"If you don't have a university-level transcript for the subjects you want to tutor, attach your matric results instead.", null=True, verbose_name=b'Academic transcript')),
                ('cv', models.ForeignKey(related_name='cv_tutors', verbose_name=b'CV', blank=True, to='common.Document', null=True)),
                ('id_doc', models.ForeignKey(related_name='id_tutors', verbose_name=b'ID', to='common.Document', help_text=b'Identification document with a photo is required.', null=True)),
                ('subject', models.ManyToManyField(to='option.AvailableTutorSubject', verbose_name=b'subject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
