# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiningOAM', '0006_auto_20160229_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authusergroups',
            options={'managed': False},
        ),
    ]
