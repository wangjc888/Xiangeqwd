from __future__ import absolute_import

from celery import shared_task
from DiningOAM.models import TblMealInHouse

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def testPrint():
    print('开始任务')
    pass


#回复估清，在settings.py中设置对应的恢复估清时间
@shared_task
def regainMealStatus():
    print('恢复估清的菜品')
    mealSet = TblMealInHouse.objects.filter(meal_status=0).update(meal_status=1)#刷新订单状态全部为1
    print('mealSet: ', mealSet)
    pass
