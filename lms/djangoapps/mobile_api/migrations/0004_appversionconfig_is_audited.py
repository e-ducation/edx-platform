# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-12 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api', '0003_ignore_mobile_available_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='appversionconfig',
            name='is_audited',
            field=models.BooleanField(default=False),
        ),
    ]
