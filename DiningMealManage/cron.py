__author__ = 'liujiazhi'
from DiningMealManage.models import TblBill
from DiningMealManage.models import TblBillMeal
from DiningMealManage.models import TblUser
import datetime
from datetime import timedelta
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


(NO_DEFAULT,SET_DEFAULT)=range(2)
user_status = [
            (NO_DEFAULT, '非默认地址'),
            (SET_DEFAULT,'默认地址'),
            ]

def schduled_push(local_id):
    print('enter in schduled_push:local_id: ', local_id)
    bill_list = []
    meal_list = []
    user_list = []
    billDict = {}
    #时间需要限定为今天，当前的订单状态需要限定为1，即支付完成状态
    now = datetime.datetime.today()
    print ('schduled_push: now',now)
    print ('strftime: ',now.strftime('%d'))
    billSet = TblBill.objects.filter( house_id = local_id, add_time__day = now.strftime('%d'), bill_state = 1)#add时间等于给定的显示时间
    for item in billSet:
        print('billSet: ',billSet)
        if item.id:
            detailSet = TblBillMeal.objects.filter(bill_id=item.id)
            for key in detailSet:
                mealDict = {
                    'meal_name' :key.meal_name,
                    'buy_count' :key.buy_count,
                    'meal_price':key.meal_price,#这里的price是单价还是对应菜品的总价？
                }
                meal_list.append(mealDict)
            print('schduled_push/user_id', item.user_id)
            userSet = TblUser.objects.filter(id=item.user_id)[0]
            print('username', userSet.username)

            # try:
            #     print('enter try')
            #     userSet = TblUser.objects.get(openid=item.openid, default=SET_DEFAULT)[0]
            # except:
            #     print('enter except')
            #     userSet = TblUser.objects.filter(openid=item.openid)[0]
            # print('username', userSet.username)
            user_list.append({'username':userSet.username, 'phone':userSet.phone})
            # userSet = TblUser.objects.filter(openid=item.openid)
            # for key1 in userSet:
            #     print()
            #     userDict = {
            #         'username': key1.username,
            #         'phone':key1.phone,
            #     }
            #     user_list.append(userDict)
            billDict = {
                'id':item.id,
                #'prepay_id' : item.prepay_id,
                'house_id' : item.house_id,
                'openid' :item.openid,
                'user_location' : userSet.user_location,
                #'user_location' : item.user_location,
                #'bill_totalling' : item.bill_totalling,
                'delivery_fee':item.delivery_fee,
                'all_fee' : item.all_fee,
                # 'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
                # 'pay_time' : item.pay_time.strftime('%Y-%m-%d %H:%I:%S'),
                'bill_state' : item.bill_state,
                'bill_content' : item.bill_content,
                # 'ensure_send_time' : item.ensure_send_time.strftime('%Y-%m-%d %H:%I:%S')
                'meal_detail':meal_list,
                'user_detail':user_list,
            }
            if not item.add_time:
                billDict['add_time']=0
            else:
                billDict['add_time']=item.add_time.strftime('%Y-%m-%d %H:%M:%S')
            bill_list.append(billDict)
            meal_list = []#清空菜品相关的列表
            user_list = []#情况用户相关列表

    # print('bill_list:', bill_list)
    return {'bill_list': bill_list}

def updateBillState(local_id, post):
    print('enter in updateBillState')
    bill_id = post.get('bill_id',None)
    house_id = post.get('house_id', None)
    flag = post.get('flag', None)#判定是确定还是取消
    openid = post.get('openid', None)

    print ('house_id:', house_id, 'local_id:', local_id, 'flag:', flag ,'type:', type(flag), 'bill_id:',bill_id)
    if house_id == local_id:
        if flag == '1':
            print ('enter flag = 1 ')
            TblBill.objects.filter(house_id=house_id, id=bill_id, bill_state=1).update(bill_state=2)
        else:
            print ('enter flag')
            TblBill.objects.filter(house_id=house_id, id=bill_id, bill_state=1).update(bill_state=3)#对应订单取消状态
        testSet = TblBill.objects.filter(house_id=house_id, id=bill_id)
        for item in testSet:
            print('item: ',item.bill_state)
        return 'success'
    else:
        return 'fail'


def insert_to_record(local_id, post):
    print('insert_to_record')
    order_list = []
    house_id = post.get('house_id', None)
    flag = post.get('flag', None)
    print('house_id:', house_id, 'local_id:', local_id,'flag: ',flag)
    if house_id == local_id:
        if flag == '1':#确认的订单
            # recordSet = TblBill.objects.filter(house_id=house_id, bill_state__gte=2, bill_state__lte=4).order_by('-add_time')#订单状态大于1，小于4
            #recordSet = TblBill.objects.filter(Q(house_id=house_id)&Q(bill_state=2)|Q(bill_state__gte=4)).order_by('-add_time')#订单状态为2，或大于等于4#add at 03-02
            recordSet = TblBill.objects.filter(Q(house_id=house_id)&Q(bill_state=2)|Q(bill_state=4)).order_by('-add_time')#订单状态为2，或大于等于4
        else:
            recordSet = TblBill.objects.filter(house_id=house_id, bill_state=3).order_by('-add_time')#订单状态为3，即取消的订单

        for item in recordSet:
            recDict = {
                'bill_id':item.id,
                #'total':item.bill_totalling,
                'total':item.all_fee,
                'add_time':item.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            }

            order_list.append(recDict)
    print ('flag:', flag, 'order_list:', order_list)
    return {'order_list': order_list, 'flag':flag}

def printOrder(post):
    order_id = post.get('order_id', None)
    order_content = []
    orderDict = {}
    print('enter printOrder: order_id: ',order_id)
    orderSet = TblBill.objects.filter(id=order_id)
    for item in orderSet:
        openid = item.openid
        userSet = TblUser.objects.filter(openid=openid)
        for item2 in userSet:
            username = item2.username
            phone = item2.phone
            sex = item2.sex
        mealSet = TblBillMeal.objects.filter(bill_id=item.id)
        for item3 in mealSet:
            mealContent = {
                'name':item3.meal_name,
                'count':item3.buy_count,
                'price':item3.meal_price
            }
            order_content.append(mealContent)
        orderDict = {
            'order_id':item.id,
            'add_time':item.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            #'total':item.bill_totalling,
            'delivery_fee':item.delivery_fee,
            'total':item.all_fee,
            'user_name':username,
            'user_phone':phone,
            'user_sex':sex,
            'address':item.user_location,
            'order_content':order_content
            # 'order_content':[{'name':'土豆牛肉fan', 'count':2, 'price':'1.1'}, {'name':'土豆牛肉mian', 'count':1, 'price':'0.8'}],
        }
    #print('enter orderDict,', orderDict)
    return orderDict

def getOrderDetails(house_id, post):
    print('enter in getOrderDetails/house_id:', house_id, 'post:', post)
    orderDict = {}
    meal_list = []
    order_id = post.get('order_id', None)
    if order_id:
        orderSet = TblBill.objects.filter(id=order_id)[0]
        print('user_id', orderSet.user_id)
        userSet = TblUser.objects.filter(id=orderSet.user_id)[0]#收货人信息
        mealSet = TblBillMeal.objects.filter(bill_id=orderSet.id)#菜品内容
        print('getOrderDetails/mealSet', mealSet)
        for key in mealSet:
            mealDict = {
                'meal_name' :key.meal_name,
                'buy_count' :key.buy_count,
                'meal_price':key.meal_price,#这里的price是单价还是对应菜品的总价？
            }
            meal_list.append(mealDict)
        print('getOrderDetails/meal_list: ', meal_list)
        orderDict = {
            'id':order_id,
            'house_id' : house_id,
            'openid' :orderSet.openid,
            'username':userSet.username,
            'phone':userSet.phone,
            'user_location' : userSet.user_location,
            #'bill_totalling' : item.bill_totalling,
            'delivery_fee':orderSet.delivery_fee,
            'all_fee' : orderSet.all_fee,
            'bill_state' : orderSet.bill_state,
            'bill_content' : orderSet.bill_content,
            # 'ensure_send_time' : item.ensure_send_time.strftime('%Y-%m-%d %H:%I:%S')
            'meal_detail':meal_list,
            'add_time':orderSet.add_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        print('getOrderDetails fail')
    #print('getOrderDetails/order:', orderDict)
    return {'orderDict': orderDict}


def orderSure(post):
    print('enter orderSure')
    order_id = post.get('order_id', None)
    house_id = post.get('house_id', None)
    try:
        TblBill.objects.filter(id=order_id).update(bill_state=4)#确认送达，将订单状态改为待评价
        print('orderSure/确认订单已送达')
        return {'result':'success'}
    except ObjectDoesNotExist:
        print('orderSure/订单处理异常，请重试')
        return {'result':'fail', 'atach_info':'订单处理异常，请重试'}

    # if order_id:
    #     print('orderSure/确认订单已送达')
    #     TblBill.objects.filter(id=order_id).update(bill_state=4)#确认送达，将订单状态改为待评价
    #     return {'result':'success'}
    # else:
    #     return {'result':'fail', 'atach_info':'订单处理异常，请重试'}