from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session

from DiningServer.models import *
from DiningServer import interface
from DiningServer.service import meal_service,user_service

from DiningServer.common.time_format_util import SERVER_TIME_FORMAT_WITHOUT_SECOND
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from DiningServer.common.func import *

from uuid import uuid4
import time


"""
订单相关服务
"""

(BILL_STATE_UNPAY,BILL_STATE_PAY,BILL_STATE_SENDING,BILL_STATE_REFUND,BILL_STATE_OVER,BILL_STATE_JUDGED)=range(6)
bill_state = [
            (BILL_STATE_UNPAY,'未付款'),
            (BILL_STATE_PAY,'已付款'),
            (BILL_STATE_SENDING,'配送中'),
            (BILL_STATE_REFUND,'已退款'),
            (BILL_STATE_OVER,'已完成'),
            (BILL_STATE_JUDGED,'已评价'),
            ]

(ALLOW,DENY)=range(2)
bill_access = [
            (ALLOW, '允许'),
            (DENY,'禁止'),
            ]

def createOrder(request):
    openid = request.session.get('openid','openiddefault')
    print('openid before createOrder:',openid)
    try:
        user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-add_time')[0]
    except:
        user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]

    print('user_id in bill:',user.id)
    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    meals = meal_service.getMealsAndCount(request.POST)
    # count = 0
    sum = 0

    buy_meals = meals['meal_list']

    # 获取sum和count
    for meal in buy_meals:
        # count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])

    #配送费
    # delivery_fee = getDeliveryFee(request, sum)
    delivery_fee = float(0.01)

    # 创建订单
    bill = TblBill()
    bill.id = uuid4()
    bill.house_id = request.session.get('house_id','houseiddefault')
    bill.openid = request.session.get('openid','openiddefault')
    bill.user_id = user.id
    bill.user_location = user.user_location
    bill.door = user.door
    bill.bill_totalling = sum
    bill.delivery_fee = delivery_fee
    bill.all_fee = float(sum) + float(delivery_fee)
    bill.add_time = time_now
    bill.bill_state = BILL_STATE_UNPAY
    bill.access = ALLOW
    bill.save()
    
    return bill
"""
配送费
"""
def getDeliveryFee(request, sum):
    openid = request.session.get('openid','openiddefault')
    try:
        user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-add_time')[0]
    except:
        user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]

    house_id = request.session.get('house_id','houseiddefault')
    house = TblHouse.objects.filter(id=house_id)[0]

    print('user.longitude:',user.longitude)
    print('user.latitude:',user.latitude)
    print('house.longitude:',user.longitude)
    print('house.latitude:',user.latitude)

    distance = haversine(user.longitude, user.latitude, house.longitude, house.latitude)
    print('distance:',distance)
    if float(distance) <= float(3):
        print('distance1???')
        if float(sum) <= float(40):
            delivery_fee = float(4)
        elif float(sum) > float(40) and float(sum) <= float(200):
            delivery_fee = float(sum*0.1)
        elif float(sum) > float(200):
            delivery_fee = float(20)
    else:
        print('distance2???')
        if float(sum) <= float(40):
            delivery_fee = float(4) + float(2*(int(distance)+1))
        elif float(sum) > float(40) and float(sum) <= float(200):
            delivery_fee = float(sum*0.1) + float(2*(int(distance)+1))
        elif float(sum) > float(200):
            delivery_fee = float(20) + float(2*(int(distance)+1))

    return delivery_fee


from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


"""
如果支付成功 则返回非None 如果失败 返回None
"""
def payOrder(request,bill_id,pay_result):

    # 查询订单状态 如果不是等待支付 则返回对应的订单的状态
    bill = TblBill.objects.get(id=bill_id)
    if bill.bill_state != BILL_STATE_UNPAY:
        return None

    # 如果支付成功
    if pay_result:
        bill.bill_state = BILL_STATE_PAY
        bill.pay_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        bill.save()
    else: return None

"""
支付完成后跳转到用户订单页面
"""
def getOrders(bill_id, openid):

    myOrder = TblBill.objects.filter(id=bill_id, openid=openid)
    myBill = MyBill()
    for item in myOrder:
        if item.add_time:
            add_time = item.add_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        else: add_time = None
        
        if item.pay_time:
            pay_time = item.pay_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        else: pay_time = None
        
        if item.ensure_send_time:
            ensure_send_time = item.ensure_send_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        else: ensure_send_time = None

        myBillIndex = myBill.createBill(
            item.id,
            item.prepay_id,
            item.house_id,
            item.openid,
            item.user_location,
            item.bill_totalling,
            add_time,
            pay_time,
            item.bill_state,
            item.bill_content,
            ensure_send_time,
            meals
        )

        myMeals = TblBillMeal.objects.filter(bill_id=item.id)
        for meal in myMeals:
            myBill.addMeal(myBillIndex, meal.house_id, meal.meal_name, meal.meal_url, meal.buy_count, meal.meal_price)
            
    return myBill.toDict()

"""
获取用户所有订单，根据用户输入的用户id和订单状态（未付款，派送中，待评价）返回用户订单列表
"""
def getMyBills(openid):
    myBills = interface.MyBills()
    allBill = TblBill.objects.filter(openid=openid,access=ALLOW).order_by('-add_time')

    for bill in allBill:
        index = myBills.createMyBill(
                                    bill.id, 
                                    bill.prepay_id, 
                                    bill.house_id, 
                                    bill.openid, 
                                    bill.user_id, 
                                    bill.user_location, 
                                    bill.door, 
                                    bill.bill_totalling, 
                                    bill.delivery_fee, 
                                    bill.all_fee, 
                                    bill.add_time, 
                                    bill.pay_time, 
                                    bill.bill_state, 
                                    bill.bill_content, 
                                    bill.ensure_send_time
                                    )

        myMeals = TblBillMeal.objects.filter(bill_id=bill.id)
        for meal in myMeals:
            myBills.addMeal(
                            meal.id, 
                            meal.meal_id, 
                            meal.house_id, 
                            meal.bill_id, 
                            meal.openid, 
                            meal.user_id, 
                            meal.buy_count, 
                            meal.add_time, 
                            meal.meal_name, 
                            meal.meal_url, 
                            meal.meal_price, 
                            index)

        try:
            house = TblHouse.objects.filter(id=bill.house_id)[0]
        except:
            house = {}

        myBills.addHouse(
                        house.id, 
                        house.name, 
                        house.latitude, 
                        house.longitude, 
                        house.location, 
                        house.add_time, 
                        house.phone, 
                        index)
    return myBills.toDict()
    

"""
获取某个订单详情
"""
def getBillDetail(bill_id):
    billDetail = interface.billDetail()
    try:
        tbl_bill = TblBill.objects.filter(id=bill_id)[0]
    except:
        return {}

    billDetail.getBillDetail(
                            tbl_bill.id, 
                            tbl_bill.prepay_id, 
                            tbl_bill.house_id, 
                            tbl_bill.openid, 
                            tbl_bill.user_id, 
                            tbl_bill.user_location, 
                            tbl_bill.door, 
                            tbl_bill.bill_totalling, 
                            tbl_bill.delivery_fee, 
                            tbl_bill.all_fee, 
                            tbl_bill.add_time, 
                            tbl_bill.pay_time, 
                            tbl_bill.bill_state, 
                            tbl_bill.bill_content, 
                            tbl_bill.ensure_send_time
                            )


    myMeals = TblBillMeal.objects.filter(bill_id=bill_id)
    for meal in myMeals:
        billDetail.addMeal(
                        meal.id, 
                        meal.meal_id, 
                        meal.house_id, 
                        meal.bill_id, 
                        meal.openid, 
                        meal.user_id, 
                        meal.buy_count, 
                        meal.add_time, 
                        meal.meal_name, 
                        meal.meal_url, 
                        meal.meal_price, 
                        )

    # try:
    #     house = TblHouse.objects.filter(id=tbl_bill.house_id)[0]
    # except:
    #     house = {}
        
    # billDetail.addHouse(
    #                 house.id, 
    #                 house.name, 
    #                 house.latitude, 
    #                 house.longitude, 
    #                 house.location, 
    #                 house.add_time, 
    #                 house.phone, 
    #                 index)
    return billDetail.toDict()


# 确认送达 可有商户或者用户两方调用
def ensureSend(bill_id):

    # 如果不是正在派送的状态，则返回失败
    if bill.bill_state != BILL_STATE_SENDING:
        return False

    try:
        bill = TblBill.objects.get(id=bill_id)
    except ObjectDoesNotExist:
        return False
    else:
        # 更改状态为待评价
        bill.bill_state = BILL_STATE_JUDGE
        bill.ensure_send_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        bill.save()
        return True
    return False


def getHouseJudgeSet(house_id):
    houseJudgeSet = interface.getHouseJudgeSet()
    print('initial getHouseJudgeSet...')
    tbl_judge_meal = []
    # tbl_judge_meal = TblJudgeMeal.objects.filter(house_id=house_id).order_by('-add_time').values('bill_id').distinct()
    billSet = set(TblJudgeMeal.objects.filter(house_id=house_id).values_list('bill_id',flat=True))
    for bill_id in billSet:
        tjmObj = TblJudgeMeal.objects.filter(house_id=house_id,bill_id=bill_id).order_by('-add_time')[0]
        tbl_judge_meal.append(tjmObj)

    for item in tbl_judge_meal:
        print(item)
        index = houseJudgeSet.addJudgeToHouse(
                                            item.id, 
                                            item.house_id, 
                                            item.bill_id, 
                                            item.meal_id, 
                                            item.user_id, 
                                            item.judge_meal, 
                                            item.judge_speed, 
                                            item.judge_message, 
                                            item.add_time
                                            )
        houseJudgeSet.calJudge(item.judge_meal, item.judge_speed)
        houseJudgeSet.setJudgeType(item.judge_meal, item.judge_speed, index)

        tbl_user = TblUser.objects.filter(id=item.user_id)[0]
        houseJudgeSet.setUserPhone(tbl_user.phone, index)

    house = TblHouse.objects.filter(id=house_id)[0]
    houseJudgeSet.getHouse(
                        house.id, 
                        house.name, 
                        house.latitude, 
                        house.longitude, 
                        house.location, 
                        house.add_time, 
                        house.phone
                        )

    return houseJudgeSet.toDict()