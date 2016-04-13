# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiningServer', '0004_auto_20160229_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authusergroups',
            options={'managed': False},
        ),
    ]
