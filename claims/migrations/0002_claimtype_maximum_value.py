# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
                model_name='claimtype',
                name='maximum_value',
                field=models.FloatField(default=1, help_text='The maximum claim_value a claim of this type can hold'),
        ),
    ]
