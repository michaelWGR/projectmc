# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-07-24 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='path',
            field=models.CharField(max_length=512),
        ),
    ]
