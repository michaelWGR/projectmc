# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-08-02 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20180731_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCRResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.CharField(db_index=True, max_length=16)),
                ('items', models.TextField(null=True)),
                ('is_error', models.IntegerField(default=0)),
                ('errors', models.TextField(null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('mtime', models.DateTimeField(auto_now=True)),
                ('remark', models.TextField(null=True)),
                ('resource', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='management.Resource')),
            ],
            options={
                'db_table': 'ocr_results',
            },
        ),
        migrations.CreateModel(
            name='PornResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.CharField(db_index=True, max_length=16)),
                ('label', models.IntegerField(default=0)),
                ('rate', models.FloatField(default=0.0)),
                ('is_review', models.IntegerField(default=0)),
                ('is_error', models.IntegerField(default=0)),
                ('errors', models.TextField(null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('mtime', models.DateTimeField(auto_now=True)),
                ('remark', models.TextField(null=True)),
                ('resource', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='management.Resource')),
            ],
            options={
                'db_table': 'porn_results',
            },
        ),
    ]
