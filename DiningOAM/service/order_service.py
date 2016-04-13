__author__ = 'liujiazhi'

from DiningOAM.models import TblBill
#from django.utils.timezone import now, timedelta
import time
import datetime
from datetime import timedelta
from DiningOAM.models import TblAdminuser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

#需要提供时间列表(提供的是每日的订单总量统计，不是累加值)
def orderCount(post):
    # print('orderCount===================')
    order_count = {'date_list':[], 'count_list':[]}
    countDict = {}
    min_time = post.get('min', 1)#如果没有输入参数
    max_time = post.get('max', 1)

    if min_time == 1 and max_time == 1:
    # if len(post) == 0:#如果没有提供时间则默认输出近一周统计(是一个累加值)
        for key in range(7):
            end_time = datetime.datetime.today() - timedelta(days = key)
            daliy_num = TblBill.objects.filter(add_time__day = end_time.strftime('%d'), bill_state__gte = 1).count()#add时间等于给定的显示时间
            #countDict[key+1] = {'Date': end_time.strftime('%Y-%m-%d'), 'Cnt': daliy_num}
            order_count['date_list'].append(end_time.strftime('%Y-%m-%d'))
            order_count['count_list'].append(daliy_num)
    else:
        # min_time = post['min']
        # max_time = post['max']
        # print('min:', min_time, 'max:', max_time, 'type:', type(min_time))
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        key = 0
        while end_time - timedelta(days = key) > start_time:
            daliy_time = end_time - timedelta(days = key)
            #countDict['daliy_time'] = TblBill.objects.filter(add_time = end_time, bill_state__gt = 1).count()
            key += 1
            num = TblBill.objects.filter(add_time__day = daliy_time.strftime('%d'), bill_state__gte = 1).count()
            #countDict[key] ={'Date': daliy_time.strftime('%Y-%m-%d'), 'Cnt': num }
            order_count['date_list'].append(daliy_time.strftime('%Y-%m-%d'))
            order_count['count_list'].append(daliy_num)
            #print('countDict', countDict)

    order_count['date_list'].reverse()
    order_count['count_list'].reverse()
    # print('orderCount:', order_count)
    #return {'countDict': countDict}
    return order_count

#返回一个时间段内所有记录（逐条列出）
def orderList(logname, post):
    order_list = []
    house_info = []
    try:
        orderSet = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = orderSet.getHouseId()
        userType = orderSet.getUserType()#获取当前用户的类型
        house_name = orderSet.getHouseName()
    except ObjectDoesNotExist:
        return None

    min_time = post.get('min', None)
    max_time = post.get('max', None)
    house_id = post.get('house_id', local_id)#如果当前没有选择当前的店面，则显示所有

    print('min:', min_time, 'max:', max_time, 'house_id:', house_id, 'local_id', local_id)
    if min_time == None and max_time == None:
        print ('return tblBill.objects.filter')
        order_list_set = TblBill.objects.filter(house_id=house_id, bill_state__gte = 1).order_by('-add_time')
        print('==============================')
    else:
        print('min:', min_time, 'max:', max_time, 'type:', type(min_time))
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        # print('start_time:', start_time, 'end_time:', end_time)
        #print('type:', type(test))
        #for key in test:
        #    order_list
        #    print('test_id', key.id, 'add_time:', key.add_time)
        order_list_set = TblBill.objects.filter(house_id=house_id, bill_state__gte = 1, add_time__gte = start_time, add_time__lte = end_time).order_by('-add_time')
    #   order_list_set = TblBill.objects.filter(Q(add_time__gte = start_time) & Q(add_time__lte = end_time) | Q(house_id=house_id) & Q(bill_state__gte = 1))#for test Q-object
    for item in order_list_set:
        if item.id:
            print('pay_time:', item.pay_time)
            bill_list = {
                'id' : item.id,
                'prepay_id' : item.prepay_id,
                # 'code_url' : item.code_url,#字段被删除
                'house_id' : item.house_id,
                # 'user_id' : item.user_id,#字段被修改
                'openid' :item.openid,
                # 'user_location' : item.user_location,
                'bill_totalling' : item.bill_totalling,
                # 'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
                # 'pay_time' : item.pay_time.strftime('%Y-%m-%d %H:%I:%S'),
                'bill_state' : item.bill_state,
                'bill_content' : item.bill_content,
                # 'ensure_send_time' : item.ensure_send_time.strftime('%Y-%m-%d %H:%I:%S')
            }
            if not item.add_time:
                bill_list['add_time']=0
            else:
                bill_list['add_time']=item.add_time.strftime('%Y-%m-%d %H:%I:%S')
            if not item.pay_time:
                bill_list['pay_time']=0
            else:
                bill_list['pay_time']=item.pay_time.strftime('%Y-%m-%d %H:%I:%S')
            if not item.ensure_send_time:
                bill_list['ensure_send_time']=0
            else:
                bill_list['ensure_send_time']=item.ensure_send_time.strftime('%Y-%m-%d %H:%I:%S')

            order_list.append(bill_list)
            print('order_list:', order_list)
    # return {'order_list': order_list,'order_count':len(order_list)}
    if house_id == local_id:
        house_info.append({'house_id':local_id, 'house_name': house_name})
    else:
        try:
            orderSet1 = TblAdminuser.objects.get(house_id = house_id)
            search_name = orderSet1.getHouseName()
            house_info.append({'house_id':house_id, 'house_name': search_name})
        except ObjectDoesNotExist:
            return None
    logSet = TblAdminuser.objects.all()
    for item in logSet:
        if item.house_id != house_id:
            house_info.append({'house_id':item.house_id, 'house_name': item.house_name})
    return {'order_list': order_list,'order_count':len(order_list), 'house_info':house_info}

def delOrderInfo(logname, orderId):
    order_list = []
    try:
        orderSet = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = orderSet.getHouseId()
        userType = orderSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return {'result':'fail', 'atach_info':'请重新登录'}
        #return None

    toDelData = TblBill.objects.filter(house_id=local_id, id=orderId)
    if toDelData:
        print('enter order_delete')
        toDelData.delete()
        # order_list_set = TblBill.objects.filter(house_id=local_id, bill_state__gte = 1).order_by('-add_time')
        # for item in order_list_set:
        #     if item.id:
        #         print('pay_time:', item.pay_time)
        #         bill_list = {
        #             'id' : item.id,
        #             'prepay_id' : item.prepay_id,
        #             'code_url' : item.code_url,
        #             'house_id' : item.house_id,
        #             'user_id' : item.user_id,
        #             'bill_totalling' : item.bill_totalling,
        #             'bill_state' : item.bill_state,
        #             'bill_content' : item.bill_content,
        #         }
        #         if not item.add_time:
        #             bill_list['add_time']=0
        #         else:
        #             bill_list['add_time']=item.add_time.strftime('%Y-%m-%d %H:%I:%S')
        #         if not item.pay_time:
        #             bill_list['pay_time']=0
        #         else:
        #             bill_list['pay_time']=item.pay_time.strftime('%Y-%m-%d %H:%I:%S')
        #         if not item.ensure_send_time:
        #             bill_list['ensure_send_time']=0
        #         else:
        #             bill_list['ensure_send_time']=item.ensure_send_time.strftime('%Y-%m-%d %H:%I:%S')
        #         order_list.append(bill_list)
        #         print('order_list:', order_list)
    # return {'order_list': order_list ,'order_count': len(order_list)}
        return {'result':'success'}
    else:
        print('toDelData is null')
        return {'result': 'fail', 'atach_info': '删除失败，请重试'}



