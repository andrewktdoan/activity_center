# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20171121_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planner', to='activity.User'),
        ),
    ]
