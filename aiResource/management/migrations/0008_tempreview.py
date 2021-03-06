# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-26 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_ocrresult_pornresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempReview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review_status', models.IntegerField(default=0)),
                ('old_value', models.IntegerField(null=True)),
                ('new_value', models.IntegerField(null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('mtime', models.DateTimeField(auto_now=True)),
                ('resource', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='management.Resource')),
            ],
            options={
                'db_table': 'temp_reviews',
            },
        ),
    ]
