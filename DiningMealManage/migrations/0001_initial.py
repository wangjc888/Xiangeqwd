# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group',
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group_permissions',
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_permission',
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_groups',
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_user_permissions',
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_admin_log',
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'django_content_type',
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(serialize=False, max_length=40, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_session',
            },
        ),
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
                'managed': False,
                'db_table': 'tbl_adminuser',
            },
        ),
        migrations.CreateModel(
            name='TblBanner',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('banner_url', models.CharField(max_length=300)),
                ('link_url', models.CharField(max_length=300)),
                ('show_order', models.IntegerField(null=True, blank=True)),
                ('in_use', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_banner',
            },
        ),
        migrations.CreateModel(
            name='TblBill',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('prepay_id', models.CharField(null=True, blank=True, max_length=36)),
                ('house_id', models.CharField(null=True, blank=True, max_length=36)),
                ('openid', models.CharField(max_length=36)),
                ('user_location', models.CharField(max_length=300)),
                ('bill_totalling', models.IntegerField(null=True, blank=True)),
                ('add_time', models.DateTimeField()),
                ('pay_time', models.DateTimeField(null=True, blank=True)),
                ('bill_state', models.IntegerField()),
                ('bill_content', models.CharField(null=True, blank=True, max_length=300)),
                ('ensure_send_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_bill',
            },
        ),
        migrations.CreateModel(
            name='TblBillMeal',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('house_id', models.CharField(max_length=36)),
                ('bill_id', models.CharField(max_length=36)),
                ('buy_count', models.IntegerField(null=True, blank=True)),
                ('add_time', models.DateTimeField()),
                ('meal_name', models.CharField(max_length=300)),
                ('meal_url', models.CharField(max_length=300)),
                ('meal_price', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_bill_meal',
            },
        ),
        migrations.CreateModel(
            name='TblHouse',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.CharField(max_length=300)),
                ('add_time', models.DateTimeField(null=True, blank=True)),
                ('phone', models.CharField(null=True, blank=True, max_length=20)),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_house',
            },
        ),
        migrations.CreateModel(
            name='TblJudgeMeal',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('house_id', models.CharField(max_length=36)),
                ('bill_id', models.CharField(max_length=36)),
                ('meal_in_house', models.CharField(max_length=36)),
                ('openid', models.CharField(max_length=36)),
                ('user_name', models.CharField(null=True, blank=True, max_length=300)),
                ('judge_meal', models.IntegerField()),
                ('judge_speed', models.IntegerField()),
                ('judge_service', models.IntegerField()),
                ('add_time', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_judge_meal',
            },
        ),
        migrations.CreateModel(
            name='TblMeal',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('house_id', models.CharField(max_length=36)),
                ('category_id', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=300)),
                ('avatar_url', models.CharField(max_length=300)),
                ('meal_price', models.FloatField()),
                ('detail_content', models.CharField(max_length=900)),
                ('add_time', models.DateTimeField()),
                ('category_order', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_meal',
            },
        ),
        migrations.CreateModel(
            name='TblMealCategory',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('change_time', models.DateTimeField(null=True, blank=True)),
                ('show_order', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_meal_category',
            },
        ),
        migrations.CreateModel(
            name='TblMealInHouse',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('meal_id', models.CharField(max_length=36)),
                ('house_id', models.CharField(max_length=36)),
                ('category_id', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=100)),
                ('avatar_url', models.CharField(max_length=300)),
                ('detail_url', models.CharField(max_length=300)),
                ('detail_content', models.CharField(max_length=900)),
                ('sold_count', models.IntegerField(null=True, blank=True)),
                ('judge_count', models.IntegerField(null=True, blank=True)),
                ('meal_price', models.FloatField()),
                ('last_count', models.IntegerField(null=True, blank=True)),
                ('add_time', models.DateTimeField()),
                ('category_order', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_meal_in_house',
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
                'managed': False,
                'db_table': 'tbl_meal_price',
            },
        ),
        migrations.CreateModel(
            name='TblUser',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('openid', models.CharField(max_length=36)),
                ('username', models.CharField(max_length=300)),
                ('sex', models.IntegerField(null=True, blank=True)),
                ('phone', models.CharField(null=True, blank=True, max_length=20)),
                ('add_time', models.DateTimeField(null=True, blank=True)),
                ('user_location', models.CharField(null=True, blank=True, max_length=300)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_user',
            },
        ),
        migrations.CreateModel(
            name='TblUserMoney',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('money', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_user_money',
            },
        ),
        migrations.CreateModel(
            name='TblUserMoneyChange',
            fields=[
                ('id', models.CharField(serialize=False, max_length=36, primary_key=True)),
                ('user_id', models.CharField(max_length=36)),
                ('left_money', models.IntegerField()),
                ('action_content', models.CharField(max_length=300)),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_user_money_change',
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
                'managed': False,
                'db_table': 'wechat_context',
            },
        ),
    ]
