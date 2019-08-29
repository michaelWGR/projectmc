# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-27 07:52
from __future__ import unicode_literals

from django.db import migrations, models


def migrating_data(apps, schema_editor):
    """
    migrating process_type to business_type
    set process_type = 0 where type 0  # no process
    set process_type = 1 where type 1  # extract
    :return:
    """
    Resource = apps.get_model("management", "Resource")
    for resources in Resource.objects.all():
        if resources.type == 0:
            resources.process_type = 0
        elif resources.type == 1:
            resources.process_type = 1
        resources.path = resources.path.strip()  # clean char '\n'
        resources.save()


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_resource_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='business_type',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(migrating_data)
    ]