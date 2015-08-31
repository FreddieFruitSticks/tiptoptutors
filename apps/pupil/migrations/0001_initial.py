# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0001_initial'),
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pupil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('contact_number', models.CharField(max_length=15)),
                ('street', models.CharField(max_length=20)),
                ('suburb', models.CharField(max_length=20)),
                ('requirement', models.TextField(null=True, verbose_name=b'personal requirements', blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(to='option.City')),
                ('level_of_study', models.ForeignKey(to='option.LevelOfStudy')),
                ('subject', models.ManyToManyField(to='option.AvailableTutorSubject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PupilTutorMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(db_index=True, null=True, blank=True)),
                ('end_date', models.DateField(db_index=True, null=True, blank=True)),
                ('price', models.CharField(max_length=20, null=True, blank=True)),
                ('lesson', models.CharField(max_length=20, null=True, verbose_name=b'number of lessons', blank=True)),
                ('pupil', models.ForeignKey(to='pupil.Pupil')),
                ('subject', models.ForeignKey(to='option.AvailableTutorSubject')),
                ('tutor', models.ForeignKey(to='tutor.Tutor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pupil',
            name='tutor',
            field=models.ManyToManyField(to='tutor.Tutor', null=True, through='pupil.PupilTutorMatch', blank=True),
            preserve_default=True,
        ),
    ]
