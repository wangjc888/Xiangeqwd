__author__ = 'liujiazhi'

from DiningOAM.models import TblUser
#from django.utils.timezone import now, timedelta
from datetime import timedelta
#from django.utils.timezone import now
import datetime
import time

#{min:'%y-%M-%d',max:'%y-%M-%d'}

def userNumber(post):#求每日的用户数
    totalNumDict = {}
    min_time = post.get('min', 1)
    max_time = post.get('max', 1)
    #if len(post) == 0:#如果没有提供时间则默认输出近一周统计
    if min_time == 1 and max_time == 1:
        for key in range(7):
            #end_time = now.date() - timedelta(days = key)
            #print('date.today:', datetime.datetime.today(), 'timedelta:', timedelta(days = key))
            end_time = datetime.datetime.today() - timedelta(days = key)
            daliyNum = TblUser.objects.filter(add_time__day = end_time).count()#add时间小于给定的显示时间
            totalNumDict[key] = {'Date': end_time.strftime('%Y-%m-%d'), 'Cnt': daliyNum }
    else:
        #min_time = post['min']
        #max_time = post['max']
        # print('min:', min_time, 'max:', max_time)
        # print(type(min_time))
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        # print('start:', start_time, 'type:', type(start_time))
        # print('end_time', end_time, 'type:', type(end_time))
        # print('end-start:', end_time-start_time)
        #print('day:', end_time.day)
        #print('month:', end_time.month)
        #print('year:', end_time.year)
        #print(end_time.replace(day = 1))
        #print('timedelta', timedelta(days = 0))
        #print(end_time - timedelta(days = 1))
        key = 0
        while end_time - timedelta(days = key) > start_time:
            daliy_time = end_time - timedelta(days = key)
            # print('daliy_time:', daliy_time)
            key += 1
            num = TblUser.objects.filter(add_time__day = daliy_time).count()
            if num:                                             #如果对应日期的订单量不为0，则以当日时间为key
                totalNumDict[key] = {'Date': daliy_time.strftime('%Y-%m-%d'), 'Cnt': num}

            # print(totalNumDict)
    return {'totalNumDict': totalNumDict}

#获取截止到某一日期的用户总量，
def userCount(post):
    countDict = {}
    min_time = post.get('min', 1)
    max_time = post.get('max', 1)
    #if len(post) == 0:#如果没有提供时间则默认输出近一周统计
    if min_time == 1 and max_time == 1:
        for key in range(7):
            end_time = now.date() - timedelta(days = key)
            daliyNum = TblUser.objects.filter(add_time__lte = end_time).count()#add时间小于给定的显示时间
            #countDict[end_time] = daliyNum
            countDict[key] = {'Date': end_time, 'Cnt': daliyNum}
    else:
        #start_time = post['min']
        #end_time = post['max'
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        # print('start:', start_time, 'type:', type(start_time))
        # print('end_time', end_time, 'type:', type(end_time))
        # print('end-start:', end_time-start_time)
        key = 0
        while end_time - timedelta(days = key) > start_time:
            daliy_time = end_time - timedelta(days = key)
            num  = TblUser.objects.filter(add_time__lte = daliy_time).count()
            countDict[key] = {'Date': daliy_time, 'Cnt': num}
            #countDict[daliy_time] = TblUser.objects.filter(add_time = end_time).count()
            key += 1

    return {'count_dict': countDict}

def userAllCountInfo(post):
    show_count_info = {'show_date_list':[], 'daliy_cnt_list':[], 'total_cnt_list':[]}
    totalNumDict = {}
    min_time = post.get('min', 1)
    max_time = post.get('max', 1)
    #if len(post) == 0:#如果没有提供时间则默认输出近一周统计
    if min_time == 1 and max_time == 1:
        for key in range(7):
            key = 6 - key
            #print('date.today:', datetime.datetime.today(), 'timedelta:', timedelta(days = key))
            end_time = datetime.datetime.today() - timedelta(days = key)
            #print('end_time',end_time,'type:', type(end_time.strftime('%Y-%m-%d')))
            totalNum = TblUser.objects.filter(add_time__lte = end_time).count()
            a = end_time.strftime('%d')
            #print('day:', a,'type:',type(a))
            #print('type(end_time):', type(end_time))
            daliyNum = TblUser.objects.filter(add_time__day = end_time.strftime('%d')).count()#add时间小于给定的显示时间
            #print('daliyNum:',daliyNum, 'totalNum:',totalNum)
            #totalNumDict[key] = {'Date': end_time.strftime('%Y-%m-%d'), 'Cnt': daliyNum }
            show_count_info['show_date_list'].append(end_time.strftime('%Y-%m-%d'))
            show_count_info['daliy_cnt_list'].append(daliyNum)
            show_count_info['total_cnt_list'].append(totalNum)
    else:
        #min_time = post['min']
        #max_time = post['max']
        # print('min:', min_time, 'max:', max_time)
        # print(type(min_time))
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        # print('start:', start_time, 'type:', type(start_time))
        # print('end_time', end_time, 'type:', type(end_time))
        # print('end-start:', end_time-start_time)
        #print('day:', end_time.day)
        #print('month:', end_time.month)
        #print('year:', end_time.year)
        #print(end_time.replace(day = 1))
        #print('timedelta', timedelta(days = 0))
        #print(end_time - timedelta(days = 1))
        key = 0
        while end_time - timedelta(days = key) > start_time:
            daliy_time = end_time - timedelta(days = key)
            print('daliy_time:', daliy_time)
            key += 1
            num = TblUser.objects.filter(add_time__day = daliy_time).count()
            if num:                                             #如果对应日期的订单量不为0，则以当日时间为key
                #totalNumDict[key] = {'Date': daliy_time.strftime('%Y-%m-%d'), 'Cnt': num}
                show_count_info['show_date_list'].append(daliy_time.strftime('%Y-%m-%d'))
                show_count_info['daliy_cnt_list'].append(daliyNum)
                show_count_info['total_cnt_list'].append(totalNum)
    # print('show_count_info:',show_count_info)
    #return {'totalNumDict': totalNumDict}
    return show_count_info



