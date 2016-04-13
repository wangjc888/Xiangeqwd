# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiningServer', '0002_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblAdminuser',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('is_super_admin', models.IntegerField()),
                ('house_id', models.CharField(max_length=36)),
                ('house_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tbl_adminuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMealPrice',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('house_id', models.CharField(max_length=36)),
                ('source_id', models.CharField(max_length=36)),
                ('add_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_meal_price',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WechatContext',
            fields=[
                ('openid', models.CharField(serialize=False, max_length=50, primary_key=True)),
                ('context_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'wechat_context',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Context',
        ),
    ]
