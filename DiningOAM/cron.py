#!/usr/bin/env python
import datetime

#django 1.6 + should add below
import os
import sys
sys.path.append('/path/to/DiningHouse/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiningHouse.settings")
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import User

#put your own code here
from DiningOAM.models import *

#code for django_cron
def my_scheduled_job():
	TblMealInHouse.objects.all().update(meal_status=1)

	with open('/path/to/django/OAMCrontab.log','a+') as f:
		f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')

# code for ubantu cron
TblMealInHouse.objects.all().update(meal_status=1)
os.system('date >> /path/to/django/OAMCrontab.log')