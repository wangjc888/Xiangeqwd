# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblBanner',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('banner_url', models.CharField(max_length=300)),
                ('link_url', models.CharField(max_length=300)),
                ('show_order', models.IntegerField(blank=True, null=True)),
                ('in_use', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_banner',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblBill',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=36)),
                ('user_location', models.CharField(blank=True, max_length=300, null=True)),
                ('bill_totalling', models.IntegerField()),
                ('add_time', models.DateTimeField()),
                ('pay_time', models.DateTimeField(blank=True, null=True)),
                ('bill_state', models.IntegerField()),
                ('bill_content', models.CharField(blank=True, max_length=300, null=True)),
                ('ensure_send_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_bill',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblBillMeal',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('bill_id', models.CharField(max_length=36)),
                ('meal_in_house_id', models.CharField(max_length=36)),
                ('buy_count', models.IntegerField()),
                ('add_time', models.DateTimeField()),
                ('name', models.CharField(max_length=300)),
                ('meal_url', models.CharField(max_length=300)),
                ('meal_price', models.FloatField()),
            ],
            options={
                'db_table': 'tbl_bill_meal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblHouse',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.CharField(max_length=300)),
                ('add_time', models.DateTimeField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'tbl_house',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblJudgeMeal',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('bill_id', models.CharField(max_length=36)),
                ('meal_in_house', models.CharField(max_length=36)),
                ('user_id', models.CharField(max_length=36)),
                ('user_name', models.CharField(blank=True, max_length=300, null=True)),
                ('judge_meal', models.IntegerField()),
                ('judge_speed', models.IntegerField()),
                ('judge_service', models.IntegerField()),
                ('add_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_judge_meal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblLocation',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=300)),
                ('add_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMeal',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('catogory_id', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=100)),
                ('avatar_url', models.CharField(max_length=300)),
                ('detail_url', models.CharField(max_length=300)),
                ('detail_content', models.CharField(max_length=900)),
                ('sold_count', models.IntegerField()),
                ('judge_count', models.IntegerField()),
                ('add_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_meal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMealCategory',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('change_time', models.DateTimeField(blank=True, null=True)),
                ('show_order', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_meal_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMealInHouse',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('meal_id', models.CharField(max_length=36)),
                ('house_id', models.CharField(max_length=36)),
                ('category_id', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=100)),
                ('avatar_url', models.CharField(max_length=300)),
                ('detail_url', models.CharField(max_length=300)),
                ('detail_content', models.CharField(max_length=900)),
                ('sold_count', models.IntegerField()),
                ('judge_count', models.IntegerField()),
                ('meal_price', models.FloatField()),
                ('last_count', models.IntegerField()),
                ('add_time', models.DateTimeField()),
                ('category_order', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_meal_in_house',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUser',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=300)),
                ('sex', models.IntegerField(blank=True, null=True)),
                ('birthday', models.DateField()),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('add_time', models.DateTimeField(blank=True, null=True)),
                ('user_location', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'tbl_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUserMoney',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('money', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_user_money',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUserMoneyChange',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=36)),
                ('left_money', models.IntegerField()),
                ('action_content', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'tbl_user_money_change',
                'managed': False,
            },
        ),
    ]
