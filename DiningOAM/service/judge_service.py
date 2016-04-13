__author__ = 'liujiazhi'
from DiningOAM.models import TblJudgeMeal
from django.core.exceptions import ObjectDoesNotExist
from DiningOAM.models import TblAdminuser
import datetime
import time
from datetime import timedelta

def getJudgeInfo(logname, post):
    judge_list = []
    house_info = []
    try:
        judgeSet = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = judgeSet.getHouseId()
        userType = judgeSet.getUserType()#获取当前用户的类型
        house_name = judgeSet.getHouseName()
    except ObjectDoesNotExist:
        return None

    min_time = post.get('min', None)
    max_time = post.get('max', None)
    house_id = post.get('house_id', local_id)

    print('min:', min_time, 'max:', max_time, 'house_id:', house_id, 'local_id', local_id)
    #如果是超级管理员,默认输出所有的评价信息
    if min_time == None and max_time == None:#无时间输入
        judge_info_set = TblJudgeMeal.objects.filter(house_id=house_id).order_by('-add_time')
        # if userType and house_id==local_id:
        #     judge_info_set = TblJudgeMeal.objects.all()
        # else:
        #     judge_info_set = TblJudgeMeal.objects.filter(house_id=house_id)
    else:
        print('min:', min_time, 'max:', max_time, 'type(min):', type(min))
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        judge_info_set = TblJudgeMeal.objects.filter(house_id=house_id, add_time__gte = start_time, add_time__lte = end_time).order_by('-add_time')
    #judge_info_set = TblJudgeMeal.objects.filter(house_id = 'local_id')#这里获取的评价信息是否需要添加时间的过滤
    # print('judge_info_set:', judge_info_set)
    for item in judge_info_set:
        if item.house_id:
            judge_info = {
                'id' : item.id,
                'house_id' : item.house_id,
                'bill_id' : item.bill_id,
                'meal_in_house' : item.meal_in_house,
                # 'user_id' : item.user_id,
                'openid':item.openid,
                'judge_meal' : item.judge_meal,
                'judge_speed': item.judge_speed,
                'judge_service' : item.judge_service,
                # 'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S')
            }
            if item.add_time == 0:
                judge_info['add_time'] = item.add_time
            else:
                judge_info['add_time'] = item.add_time.strftime('%Y-%m-%d %H:%I:%S')
            judge_list.append(judge_info)
        print('judge_list:',judge_list)

    # return {'judge_list': judge_list, 'judge_count': len(judge_list)}
    if house_id == local_id:
        house_info.append({'house_id':local_id, 'house_name': house_name})
    else:
        try:
            orderSet1 = TblAdminuser.objects.get(house_id = house_id)
            search_name = orderSet1.getHouseName()
            house_info.append({'house_id':house_id, 'house_name': search_name})
        except ObjectDoesNotExist:
            print ('enter getJudgeInfo')
            return None
    logSet = TblAdminuser.objects.all()
    for item in logSet:
        if item.house_id != house_id:
            house_info.append({'house_id':item.house_id, 'house_name': item.house_name})
    return {'judge_list': judge_list, 'judge_count': len(judge_list), 'house_info':house_info}

def judgeDistribute(logname, post):
    judge_dict = {'judge_meal':[], 'judge_speed':[], 'judge_service':[]}
    try:
        judgeSet1 = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = judgeSet1.getHouseId()
        userType = judgeSet1.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return None
    min_time = post.get('min', 1)
    max_time = post.get('max', 1)
    judge_type = post.get('judge_type', 'judge_meal')#如果获取不到评价类型，则默认返回所有
    house_id = post.get('house_id', local_id)#对应分店也可以选择
    print ('house_id:', house_id)
    score = 0
    # if min_time == 1 and max_time == 1:#无时间输入
    #     caculateJudge(house_id, judge_type, judge_dict)
    # else:
    for i in range(5):
        score = i + 1
        judge_dict['judge_meal'].append(TblJudgeMeal.objects.filter(house_id = house_id, judge_meal = score).count())#获取本分店所有评价信息
        judge_dict['judge_speed'].append(TblJudgeMeal.objects.filter(house_id = house_id, judge_speed = score).count())
        judge_dict['judge_service'].append(TblJudgeMeal.objects.filter(house_id = house_id, judge_service = score).count())
    return judge_dict
    #return {'judge_dict': judge_dict}


#用于评价相关的统计(加入时间范围，前端无该接口，未测试)
def caculateJudge(id, judgeType, dataDict, minTime=None, maxTime=None):
    score = 0
    if minTime is None or maxTime is None:
        if judgeType == 'judge_meal':
            print ('is judge_meal pie')
            if not minTime and not maxTime:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_meal'].append(TblJudgeMeal.objects.filter(house_id = id, judge_meal = score).count())
            else:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_meal'].append(TblJudgeMeal.objects.filter(house_id = id, judge_meal = score, add_time__gte = minTime, add_time__lte = maxTime).count())

        elif judgeType == 'judge_speed':
            print ('is judge_speed pie')
            if not minTime and not maxTime:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_speed'].append(TblJudgeMeal.objects.filter(house_id = id, judge_speed = score).count())
            else:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_speed'].append(TblJudgeMeal.objects.filter(house_id = id, judge_speed = score, add_time__gte = minTime, add_time__lte = maxTime).count())
        elif judgeType == 'judge_service':
            print ('is judge_service pie')
            if not minTime and not maxTime:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_service'].append(TblJudgeMeal.objects.filter(house_id = id, judge_service = score).count())
            else:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_service'].append(TblJudgeMeal.objects.filter(house_id = id, judge_service = score ,add_time__gte = minTime, add_time__lte = maxTime).count())
        else:
            print('judge_type include 3 pie')
            if not minTime and not maxTime:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_meal'].append(TblJudgeMeal.objects.filter(house_id = id, judge_meal = score).count())#获取本分店所有评价信息
                    dataDict['judge_speed'].append(TblJudgeMeal.objects.filter(house_id = id, judge_speed = score).count())
                    dataDict['judge_service'].append(TblJudgeMeal.objects.filter(house_id = id, judge_service = score).count())
            else:
                for i in range(5):
                    score = i + 1
                    dataDict['judge_meal'].append(TblJudgeMeal.objects.filter(house_id = id, judge_meal = score, add_time__gte = minTime, add_time__lte = maxTime).count())#获取本分店所有评价信息
                    dataDict['judge_speed'].append(TblJudgeMeal.objects.filter(house_id = id, judge_speed = score, add_time__gte = minTime, add_time__lte = maxTime).count())
                    dataDict['judge_service'].append(TblJudgeMeal.objects.filter(house_id = id, judge_service = score, add_time__gte = minTime, add_time__lte = maxTime).count())
    return dataDict



def delJudgeInfo(logname, post):
    print('enter delJudgeInfo:', logname)
    try:
        judgeSet = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = judgeSet.getHouseId()
        userType = judgeSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return None
    toDelMealId=post.get('id')
    house_id = post.get('house_id', local_id)#如果获取不到要删除的评价的id，则对应查找本地
    print('del_meal_id:', toDelMealId, 'house_id:', house_id)
    if userType and house_id == local_id:#超级管理员允许删除自己的评价
        judge_info_set = TblJudgeMeal.objects.filter(house_id=house_id, id=toDelMealId).delete()
        return {'result':'success'}
    else:
        #不允许删除其他店面的菜品（包括超级管理员）
        return {'result':'fail', 'atach_info':'您无权删除其他店面菜品'}