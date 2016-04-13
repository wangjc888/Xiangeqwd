# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiningMealManage', '0002_auto_20160229_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authusergroups',
            options={'managed': False},
        ),
    ]
