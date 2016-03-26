# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0006_auto_20160322_2302'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customauthuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='customauthuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customauthuser',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customauthuser',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='customauthuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Deselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='customauthuser',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='customauthuser',
            name='username',
            field=models.CharField(max_length=50, verbose_name='username', blank=True),
        ),
    ]
