# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 14:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DiningOAM', '0002_adminuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminuser',
            options={'managed': False},
        ),
    ]