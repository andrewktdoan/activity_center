# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='number_of_participants',
            new_name='qty_participants',
        ),
    ]
