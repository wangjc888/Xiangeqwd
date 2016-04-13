__author__ = 'liujiazhi'
from DiningOAM.models import TblHouse
from DiningOAM.models import TblAdminuser
from DiningOAM.models import TblBill
from DiningOAM.models import TblBillMeal
from DiningOAM.models import TblJudgeMeal
from DiningOAM.models import TblMealInHouse
from uuid import uuid4
import datetime
from django.core.exceptions import ObjectDoesNotExist

def getHouseInfo():
    #house_Info = TblHouse.object.filter(id = local_id)#根据当分店的id返回
    house_info_list = []
    house_info_set = TblHouse.objects.all().order_by('-add_time')#输出所有店面的相关信息
    print ('gerHouseInfo: ', house_info_set)
    for item in house_info_set:
        if item.id:
            house_info = {
                'id' : item.id,
                'name' : item.name,
                'latitude' : item.latitude,
                'longitude' : item.longitude,
                'location' : item.location,
                'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
                'phone' : item.phone
            }
            house_info_list.append(house_info)
            print('house_info:',house_info)
    return {'house_info_list': house_info_list ,'house_count': len(house_info_list)}

def addHouseInfo(post):
    stationDict = {}
    house_Info = TblHouse()
    house_Info.id = uuid4()
    add_name = post.get('house_name')
    flag = post.get('flag', None)#如果flag存在，且为1表示当前为修改店面信息，而非创建
    print('enter addHouseInfo:', flag)
    if flag == None:
        getSameHouse = TblHouse.objects.filter(name=add_name)
        if getSameHouse:
            print ('there is same name')
            return {'result':'fail', 'atach_info':'存在相同的店名'}
        elif not create_admin(house_Info.id, post):
            return {'result':'fail', 'atach_info':'存在相同的登录名'}
        else:
            gps_info = post.get('gps_info')
            gps_info_list = gps_info.split(",")
            print('gps:', gps_info_list)
            house_Info.name = post.get('house_name')
            house_Info.latitude = gps_info_list[0]
            house_Info.longitude = gps_info_list[1]
            house_Info.location = post.get('address')
            house_Info.phone = post.get('phone')
            house_Info.add_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%I:%S')
            print ('house_info:',house_Info)
            house_Info.save()#保存新增的分店信息
    else:
        print ('enter update info')
        house_id = post.get('house_id')
        gps_info = post.get('gps_info')
        gps_info_list = gps_info.split(",")
        print('gps:', gps_info_list)
        house_name = post.get('house_name')
        latitude = gps_info_list[0]
        longitude = gps_info_list[1]
        location = post.get('address')
        phone = post.get('phone')
        add_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%I:%S')
        print ('house_id:',house_id, 'house_name:', house_name)
        TblHouse.objects.filter(id=house_id).update(name=house_name,latitude=latitude,longitude=longitude,location=location,phone=phone,add_time=add_time)
        print('TblHouse update had finished')
        update_admin(post)
    return {'result':'success', 'atach_info': None}


def getNewHouseInfo(post):
    HouseInfoDict = {}
    for key in post:
        print(key)
        mealInfoDict[key] = post.getlist(key)
    return HouseInfoDict


def updateInfo(newHouseInfo):#找到对应id店铺信息，这里需要对id与本地id进行验证，这一点在获取时验证防止误改
    usedHouseInfo = TblHouse.objects.get(id = newHouseInfo.id)
    if len(usedHouseInfo) == 0:             #如果未找到对应id店铺信息
        return None
    else:
        usedHouseInfo.name = newHouseInfo.name
        usedHouseInfo.latitude = newHouseInfo.latitude
        usedHouseInfo.longitude = newHouseInfo.longitude
        usedHouseInfo.location = newHouseInfo.location
        usedHouseInfo.add_time = newHouseInfo.add_time
        usedHouseInfo.phone = newHouseInfo.phone
        usedHouseInfo.save()
        return 'success'

def update_admin(post):
    print('enter in update_admin')
    username = post.get('username')
    password1 = post.get('password1')
    password2 = post.get('password2')
    admintype = post.get('adminjudge')
    house_name = post.get('house_name')
    house_id = post.get('house_id')
    print('usename: ',username, 'password1:', password1, 'password2:',password2, 'admintype:',admintype, 'house_name:', house_name, 'house_id:', house_id)
    TblAdminuser.objects.filter(house_id=house_id).update(username=username, password=password1, is_super_admin=admintype, house_name=house_name)

#add for regist admin info when create new house
def create_admin(house_id, post):
    id = uuid4()
    username = post.get('username')
    password1 = post.get('password1')
    password2 = post.get('password2')
    admintype = post.get('adminjudge')
    house_name = post.get('house_name')
    print ('house_service/adminjudge:',admintype)
    getSameAccount = TblAdminuser.objects.filter(house_name=house_name)
    if username is None or password1 != password2:
        return False #创建失败
    elif getSameAccount:#存在相同的账户
        return False
    else:
        print('house_service:create success')
        TblAdminuser.objects.create(id=id, username=username, password=password1, is_super_admin=admintype,house_id=house_id, house_name=house_name)
        return True


def delHouseInfo(logname, houseId):
    house_info_list = []
    try:
        orderSet = TblAdminuser.objects.get(username = logname)#获取本地登录的权限信息
        local_id = orderSet.getHouseId()
        userType = orderSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return None
    if userType:#如果超级管理员，则有权限删除账户信息
        toDelData = TblHouse.objects.filter(id=houseId).delete()#删除登录账户信息相关所有信息
        logAccount = TblAdminuser.objects.filter(house_id=houseId).delete()
        TblBill.objects.filter(house_id=houseId).delete()
        TblBillMeal.objects.filter(house_id=houseId).delete()
        TblMealInHouse.objects.filter(house_id=houseId).delete()
        TblJudgeMeal.objects.filter(house_id=houseId).delete()

    house_info_set = TblHouse.objects.all().order_by('-add_time')#输出所有店面的相关信息
    print ('gerHouseInfo: ', house_info_set)
    for item in house_info_set:
        if item.id:
            house_info = {
                'id' : item.id,
                'name' : item.name,
                'latitude' : item.latitude,
                'longitude' : item.longitude,
                'location' : item.location,
                'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
                'phone' : item.phone
            }
            house_info_list.append(house_info)
            print('house_info:',house_info)
    return {'house_info_list': house_info_list ,'house_count': len(house_info_list)}

def getUpdateHouseInfo(post):
    houseInfoDict = {}
    house_id = post.get('house_id', None)
    print('enter getUpdateHouseInfo: house_id', house_id)
    if house_id == None:
        print('house_id is error')
    else:
        try:
            logSet = TblAdminuser.objects.get(house_id=house_id)
            username = logSet.getUserName()
            password = logSet.getPassword()
            usertype = logSet.getUserType()#获取当前用户的类型
            if usertype == '1':
                adminType = [{'value':usertype, 'type':'超级管理员'}, {'value':'0', 'type':'普通管理员'}]
                # adminType.append({'value':usertype, 'type':'超级管理员'},{'value':'0', 'type':'普通管理员'})
            else:
                adminType = [{'value':usertype, 'type':'普通管理员'}, {'value':'1', 'type':'超级管理员'}]
                # adminType.append({'value':usertype, 'type':'普通管理员'},{'value':'1', 'type':'超级管理员'})
        except ObjectDoesNotExist:
            print('there is no such house')
            return None

        houseSet = TblHouse.objects.filter(id=house_id)
        for item in houseSet:
            gpslist = str(item.latitude) +',' + str(item.longitude)
            print('gpslist', gpslist)
            houseInfoDict = {
                'house_id':item.id,
                'house_name':item.name,
                'address':item.location,
                'add_time':item.add_time,
                'phone':item.phone,
                'gpsInfo': gpslist,
                'username':username,
                'password':password,
                'adminType':adminType,
            }
    print('houseInfoDict:', houseInfoDict)
    return houseInfoDict