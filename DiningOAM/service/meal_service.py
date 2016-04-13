__author__ = 'liujiazhi'

from DiningOAM.models import TblMealInHouse
from DiningOAM.models import TblMeal
from DiningOAM.models import TblAdminuser
from DiningOAM.models import TblMealCategory
#创建的订单保存在TblMeal.TblMealInhouse为拷贝的菜品数据（当前显示的）

from DiningServer.common.time_format_util import SERVER_TIME_FORMAT_WITHOUT_SECOND
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from uuid import uuid4
import time
from django.core.exceptions import ObjectDoesNotExist
from DiningOAM.models import TblMealPrice

def mealList(username, post):
    meal_list = []
    house_info = []
    print('enter mealList:', username)
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        userType = houseSet.getUserType()#获取当前用户的类型
        house_name = houseSet.getHouseName()
    except ObjectDoesNotExist:
        return None
    print('meal_service.py/mealList: local_id:', local_id, 'userType:', userType)
    house_id = post.get('house_id', local_id)#如果获取不到id则，返回本地的id（默认）
    search_key = post.get('name', '')
    # min = post.get('min', 1)
    # max = post.get('max', 1)
    # print ('min:',min, 'max:', max, 'type(min):', type(min))
    print('meal_service.py/mealList:house_id', house_id, 'key:', search_key)

    if not search_key:
        print ('no input name')
        mealSet = TblMealInHouse.objects.filter(house_id=house_id).order_by('-add_time')
    else:
        print ('input name')
        mealSet = TblMealInHouse.objects.filter(house_id=house_id, name__contains=search_key).order_by('-add_time')
        # mealSet = TblMeal.objects.all()

    for item in mealSet:
        if item.id:
            # print('meal_service/mealList: enter forloop create base_meal')
            base_meal = {
                'id' : item.id,
                'meal_id' : item.meal_id,#meal_id弃用#(已恢复使用)
                'house_id' : item.house_id,
                'category_id' : item.category_id,
                'name' : item.name,
                'avatar_url' : item.avatar_url,
                # 'detail_url' : item.detail_url,
                'detail_content' : item.detail_content,
                # 'sold_count' : item.sold_count,
                 'judge_count' : item.judge_count,
                'meal_price' : item.meal_price,
                # 'last_count' : item.last_count,
                # 'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
                'category_order': item.category_order
            }
            if not item.add_time:
                base_meal['add_time'] = 0
            else:
                base_meal['add_time'] = item.add_time.strftime('%Y-%m-%d %H:%I:%S')

            meal_list.append(base_meal)
            # print('meal_list:', meal_list)
        else:
            continue

    if house_id == local_id:
        house_info.append({'house_id':local_id, 'house_name': house_name})
    else:
        try:
            orderSet1 = TblAdminuser.objects.get(house_id = house_id)
            search_name = orderSet1.getHouseName()
            house_info.append({'house_id':house_id, 'house_name': search_name})
        except ObjectDoesNotExist:
            print('mealList/meet ObjectDoseNotExit!!')
            return None
    logSet = TblAdminuser.objects.all()
    for item in logSet:
        if item.house_id != house_id:
            house_info.append({'house_id':item.house_id, 'house_name': item.house_name})
    print('houseInfo:', house_info)
    return {'meal_list': meal_list, 'meal_count': len(meal_list), 'house_info':house_info}


# def mealList(username, post):
#     meal_list = []
#     house_info = []
#     print('enter mealList:', username)
#     try:
#         houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
#         local_id = houseSet.getHouseId()
#         userType = houseSet.getUserType()#获取当前用户的类型
#         house_name = houseSet.getHouseName()
#     except ObjectDoesNotExist:
#         return None
#     print('meal_service.py/mealList: local_id:', local_id, 'userType:', userType)
#     house_id = post.get('house_id', local_id)#如果获取不到id则，返回本地的id（默认）
#     search_key = post.get('name', '')
#     # min = post.get('min', 1)
#     # max = post.get('max', 1)
#     # print ('min:',min, 'max:', max, 'type(min):', type(min))
#     print('meal_service.py/mealList:house_id', house_id, 'key:', search_key)
#     if userType:#如果是超级管理员，则显示TblMea
#         if not search_key:
#             # mealSet = TblMealInHouse.objects.all()
#             mealSet = TblMeal.objects.all().order_by('-add_time')
#         else:
#             mealSet = TblMeal.objects.filter(name__contains=search_key).order_by('-add_time')
#     else:
#         if not search_key:
#             print ('no input name')
#             mealSet = TblMealInHouse.objects.filter(house_id=house_id).order_by('-add_time')
#         else:
#             print ('input name')
#             mealSet = TblMealInHouse.objects.filter(house_id=house_id, name__contains=search_key).order_by('-add_time')
#             # mealSet = TblMeal.objects.all()
#
#     for item in mealSet:
#         if item.id:
#             # print('meal_service/mealList: enter forloop create base_meal')
#             base_meal = {
#                 'id' : item.id,
#                 #'meal_id' : item.meal_id,#meal_id弃用
#                 'house_id' : item.house_id,
#                 'category_id' : item.category_id,
#                 'name' : item.name,
#                 'avatar_url' : item.avatar_url,
#                 # 'detail_url' : item.detail_url,
#                 'detail_content' : item.detail_content,
#                 # 'sold_count' : item.sold_count,
#                 # 'judge_count' : item.judge_count,
#                 'meal_price' : item.meal_price,
#                 # 'last_count' : item.last_count,
#                 # 'add_time' : item.add_time.strftime('%Y-%m-%d %H:%I:%S'),
#                 'category_order': item.category_order
#             }
#             if not item.add_time:
#                 base_meal['add_time'] = 0
#             else:
#                 base_meal['add_time'] = item.add_time.strftime('%Y-%m-%d %H:%I:%S')
#
#             if userType:#如果是超级管理员则显示Tbl_meal与Tbl_meal_in_house对应关系，否则只显示meal_in_house
#                 # house_meal = TblMealInHouse.objects.filter(house_id=house_id, id=item.id)
#                 try:
#                     house_meal = TblMealInHouse.objects.get(house_id=house_id, id=item.id)
#                     judgecnt = house_meal.getJudgeCount()
#                 except ObjectDoesNotExist:
#                     continue
#                 if house_meal:
#                     base_meal['type_mark'] = 1#如果在tbl_meal_in_house中也存在同id菜品，则标记
#                     base_meal['judge_count'] = judgecnt
#                 else:
#                     base_meal['type_mark'] = 0
#                     base_meal['judge_count'] = 0
#             else:
#                 base_meal['judge_count'] = item.judge_count
#                 # base_meal['sold_count'] = item.sold_count
#                 # base_meal['last_count'] = item.last_count
#             meal_list.append(base_meal)
#             # print('meal_list:', meal_list)
#         else:
#             continue
#
#     if house_id == local_id:
#         house_info.append({'house_id':local_id, 'house_name': house_name})
#     else:
#         try:
#             orderSet1 = TblAdminuser.objects.get(house_id = house_id)
#             search_name = orderSet1.getHouseName()
#             house_info.append({'house_id':house_id, 'house_name': search_name})
#         except ObjectDoesNotExist:
#             return None
#     logSet = TblAdminuser.objects.all()
#     for item in logSet:
#         if item.house_id != house_id:
#             house_info.append({'house_id':item.house_id, 'house_name': item.house_name})
#     return {'meal_list': meal_list, 'meal_count': len(meal_list), 'house_info':house_info}

#获取更新的菜单信息，商家修改的信息
# def getUpdateInfo(post):
#     mealInfoDict = {}
#     for key in post:
#         mealInfoDict[key] = post.getlist(key)
#         print('getUpdateInfo', key, mealInfoDict[key])
#     return mealInfoDict


def updateMealInfo(pic_url, post):
    print('enter in updateMealInfo')
    meal_id = post.get('meal_id', None)
    #meal_name = post.get('meal_name', None)
    meal_name = post.get('name', None)
    meal_price = post.get('meal_price', None)
    #meal_content = post.get('meal_content', None)
    meal_content = post.get('detail_content', None)
    meal_category = post.get('category_id', None)
    house_name = post.get('house_name', None)
    print('house_name:', house_name)
    try:
        userSet = TblAdminuser.objects.get(house_name=house_name)
        house_id = userSet.getHouseId
    except ObjectDoesNotExist:
        print('对应待修改店面不存在')
        return {'result':'fail', 'atach_info':'对应待修改店面不存在,请重试'}
    #house_id = post.get('house_id', None)
    # meal_image = post.get('meal_image', None)
    # print('meal_image:', meal_image)
    try:
        TblMealInHouse.objects.get(meal_id=meal_id, house_id=house_id)
        if pic_url == None:
            TblMealInHouse.objects.filter(meal_id=meal_id, house_id=house_id).update(
                name=meal_name,
                detail_content=meal_content,
                category_id=meal_category,
                meal_price=meal_price,
                #avatar_url = avatar_url
            )
        else:#更新菜品图片
            TblMealInHouse.objects.filter(meal_id=meal_id, house_id=house_id).update(
                name=meal_name,
                detail_content=meal_content,
                category_id=meal_category,
                meal_price=meal_price,
                avatar_url = pic_url,
                detail_url = pic_url
            )
        return {'result':'success'}
    except ObjectDoesNotExist:
        print('对应待修改菜品不存在')
        return {'result':'fail', 'atach_info':'对应待修改菜品不存在,请重试'}


#这里菜品的更新，需要对应分店的id，与菜品的id
# def updateMeal(updateInfo):
#     meal_list = TblMealInHouse.objects.get(house_id = updateInfo.house_id, meal_id = updateInfo.meal_id)#更新的菜品对应分店id和菜单的id
#     if len(meal_list) == 0:#如果没有找到对应菜单，返回一个错误信息
#         return None
#         #return 'fail'
#     else:
#         meal_list.category_id = updateInfo.category_id
#         meal_list.name = updateInfo.name
#         meal_list.avatar_url = updateInfo.avatar_url
#         meal_list.detail_url = updateInfo.detail_url
#         meal_list.detail_content = updateInfo.detail_content
#         meal_list.sold_count = updateInfo.sold_count
#         meal_list.judge_count = updateInfo.judge_count
#         meal_list.meal_price = updateInfo.meal_price
#         meal_list.last_count = updateInfo.last_count
#         meal_list.add_time = updateInfo.add_time
#         meal_list.category_order = updateInfo.category_order
#
#         meal_list.save()#这里是否将更新后的数据存入到数据库中了待测试
#         return 'success'#更新到对应菜单，返回一个修改成功

#def addNewMeal(house_id, post):#直接添加到数据库里
def addNewMeal(pic_url, house_id, post):#直接添加到数据库里
    mealDict = {}
    meal_name = post.get('name')
    pic = post.get('avatar_url', None)
    print ('meal_service/addNewMeal: enter',house_id, 'meal_name:', meal_name, 'pic:', pic, 'type:', type(pic))
    meal = TblMeal.objects.filter(name=meal_name)
    user = TblAdminuser.objects.filter(house_id = house_id)
    userType = 0#默认为普通管理员
    if meal:
        print ('$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        return {'result':'fail', 'atach_info':'新增加的菜品信息和已有的菜品名重复，请返回修改'} #获取添加菜品信息失败
    else:
        print('===========================')
        mealDict['id'] = uuid4()
        mealDict['house_id'] = house_id
        cate_id = post.get('category_id')
        mealDict['category_id'] = cate_id
        mealDict['name'] = meal_name
        mealDict['avatar_url'] = post.get('avatar_url', None)
        # newMeal.detail_url = post.detail_url

        mealDict['detail_content'] = post.get('detail_content')
        # newMeal.sold_count = post.sold_count
        # newMeal.judge_count = post.judge_count
        mealDict['meal_price'] = post.get('meal_price')
        # newMeal.last_count = post.last_count
        mealDict['add_time'] = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        categorySet = TblMealCategory.objects.filter(id=cate_id)
        for item in categorySet:
            mealDict['category_order'] = item.show_order
            print('show_order:',item.show_order)
        #mealSet1 = TblMeal.objects.filter(id=id,name=meal_name)
        #mealSet2 = TblMealInHouse.objects.filter(id=id, name=meal_name)
        mealSet1 = TblMeal.objects.filter(name=meal_name)
        mealSet2 = TblMealInHouse.objects.filter(name=meal_name)
        if not mealSet1 and not mealSet2:#不存在相同菜品名称和id的情况下，才创建成功
            for item in user:
                userType = item.is_super_admin
                print('userType:',userType, 'name:', item.house_name)
            if userType:#如果是超级管理员，需要额外将数据保存到tbl_meal
                print('meal_service/addNewMeal:create success!')
                TblMeal.objects.create(
                    id=mealDict['id'],
                    house_id=mealDict['house_id'],
                    category_id=mealDict['category_id'],
                    name=mealDict['name'],
                    #avatar_url=mealDict['avatar_url'],
                    avatar_url = pic_url,
                    meal_price=mealDict['meal_price'],
                    detail_content=mealDict['detail_content'],
                    add_time=mealDict['add_time'],
                    category_order=mealDict['category_order'],
                )
                print('pic:', post.get('picture',None), 'type:', type(post.get('picture',None)))
            TblMealInHouse.objects.create(
                #id=mealDict['id'],
                id = uuid4(),
                meal_id = mealDict['id'],
                house_id=mealDict['house_id'],
                category_id=mealDict['category_id'],
                name=mealDict['name'],
                #avatar_url=mealDict['avatar_url'],
                #detail_url=mealDict['avatar_url'],
                avatar_url = pic_url,
                detail_url = pic_url,
                meal_price=mealDict['meal_price'],
                detail_content=mealDict['detail_content'],
                add_time=mealDict['add_time'],
                category_order=mealDict['category_order']
            )
            #return {'mealDict': mealDict}#可以返回做预览
            return {'result':'success'}
        else:
            return {'result':'fail', 'atach_info':'新增加的菜品信息和已有的菜品名重复，请返回修改'} #新增加的菜品信息和已有的菜品名重复，创建失败


def copyBaseMeal(house_id, post):
    print ('enter copyBaseMeal')
    #house_id = post.get('id')#当前店面的id，这里如果前端无法传递过来，则需要在view中通过getCookie('username', )来获取
    flag = post.get('flag', None)
    print('flag:',flag, 'local_id:', house_id)
    if flag == '1':#全部从数据库导入
        mealSet = TblMeal.objects.all()
        # mealCount = TblMeal.objects.all().count()#导入数据的总数
        for item in mealSet:
            add_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
            print('mealSet_id:', item.id, 'time:', add_time)
            meal = TblMealInHouse(
                id=uuid4(),
                meal_id=item.id,
                house_id=house_id,
                category_id=item.category_id,
                name=item.name,
                avatar_url=item.avatar_url,
                detail_url=item.avatar_url,
                meal_price=item.meal_price,
                detail_content=item.detail_content,
                add_time=add_time,
                category_order=item.category_order
            )
            meal.save()
            print ('MealInHouse:', meal)
            # TblMealInHouse.objects.create(
            #     id=item.id,
            #     house_id=house_id,
            #     category_id=item.category_id,
            #     name=item.name,
            #     avatar_url=item.avatar_url,
            #     detail_url=item.avatar_url,
            #     meal_price=item.meal_price,
            #     detail_content=item.detail_content,
            #     add_time=add_time,
            #     category_order=item.category_order
            # )
        return {'result':'success'}
    else:#从TblMeal导入选中的菜品
        #需要根据当前的选择菜品导入到数据库中
        print('meal_service/copyBaseMeal get house_id fail')
        return {'result':'fail'}


def delMealInfo(username, post):
    print('enter mealList:', username)
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        userType = houseSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return None

    MealId = post.get('id',)
    house_id = post.get('house_id', local_id)
    print ('house_id:', house_id, 'local_id:',local_id, 'MealId:', MealId)
    if house_id == local_id:
        #删除本地的菜品（允许）
        #delData = TblMealInHouse.objects.filter(house_id=local_id, id=MealId).delete()
        delData = TblMealInHouse.objects.filter(house_id=local_id, meal_id=MealId).delete()
        return {'result':'success', 'atach_info':''}
    else:
        #不允许删除其他店面的菜品（包括超级管理员）
        return {'result':'fail', 'atach_info':'您无权删除其他店面菜品'}




def getMealAndPrice(local_id):
    MealPriceDict = {'meal_name':[],'meal_price':[]}
    meal = {}
    priceSet = TblMealPrice.objects.all()
    mealSet = TblMealInHouse.objects.filter(house_id=local_id)
    MealPriceDict['meal_name'].append(len(mealSet))#菜品数量
    MealPriceDict['meal_price'].append(len(priceSet))#价格数量
    for item in priceSet:
        MealPriceDict['meal_price'].append({'name':item.name, 'price': item.price})

    for item in mealSet:
        meal['name'] = item.name
        meal['price'] = item.meal_price
        # print ('name:', meal)
        # MealPriceDict['meal_name'].append(meal)
        MealPriceDict['meal_name'].append({'name':item.name, 'price': item.meal_price})
    # print ('MealPriceDict:', MealPriceDict)
    #返回菜品名和对应当前的价格，和当前价格表中所有的价格
    return MealPriceDict

#返回添加的结果，成功或失败
def addNewPrice(local_id, post):
    print('enter addNewPrice')
    meal_name = post.get('meal_name', None)
    updatePrice = post.get('update_price',0)
    addPrice = post.get('new_price', 0)
    applyHouse = post.get('app_house', None)
    print('meal_service/addNewPrice: name:',meal_name, 'update:', updatePrice, 'add:', addPrice, 'apphouse:', applyHouse)
    if addPrice:
        try:
            TblMealPrice.objects.get(price=addPrice)#{'name':price_name, 'price':price1}
            # TblMealPrice.objects.get(meal_price=addPrice[1])#{'name':price_name, 'price':price1}
            print ('这里已经存在一个相同的价格')
            return {'result':'fail', 'atach_info':'存在相同的价格，请重新输入'}
        except ObjectDoesNotExist:
            price_id = uuid4()
            TblMealPrice.objects.create(id=price_id, price=addPrice, house_id=local_id)
        if meal_name != None or updatePrice != 0 or applyHouse != None:
            applyLog = applyPrice(applyHouse, meal_name, addPrice)#新建价格优先级高于在select中选中的
    else:
        applyLog = applyPrice(applyHouse, meal_name, updatePrice)#新建价格优先级高于在select中选中的
    print('addNewPrice/applyLog: ', applyLog)
    return applyLog

def updateMealPrice(house_id, house_name, post):#普通管理员只能更新本地的id
    meal_name = post.get('meal_name', null)
    updatePrice = post.get('update_price',0)
    # addPrice = post.get('new_price', 0)
    applyHouse = post.get('app_house')
    print ('appHouse:', applyHouse)
    if house_name != applyHouse:#如果不是本店
        return {'result':'fail', 'atach_info':'您无权修改其他店面菜品价格'}
    else:
        try:
            TblMealInHouse.objects.get(house_id = house_id, name=meal_name)
            TblMealInHouse.objects.filter(house_id = house_id, name=meal_name).update(meal_price=updatePrice)
            return {'result':'success'}
        except ObjectDoesNotExist:
            return {'result':'fail', 'atach_info':'当前店面无此菜品'}


#应用价格到商店
def applyPrice(house_name, meal_name, price):
    applyLog = [0]
    print('enter applyPrice: price:', price)
    toAppHouses = house_name.split(',')
    print ('applyPrice: houses: ', toAppHouses, 'type: ', type(toAppHouses))
    for key in toAppHouses:
        print ('house1:', key)
        try:
            houseSet = TblAdminuser.objects.get(house_name = key)
            house_id = houseSet.getHouseId()
            #TblMealInHouse.objects.filter(house_id = house_id, name=meal_name).update(meal_price = price)
            mealSet = TblMealInHouse.objects.get(house_id = house_id, name=meal_name)
            print ('key:',key,'enter try')
        except ObjectDoesNotExist:
            print ('key:',key,'except')
            applyLog[0] += 1
            applyLog.append({'result':'fail', 'atach_info':'更新菜品价格失败', 'house_name':key})
            continue
    # 在对价格进行应用到店面时，需要判断当前的菜品是否存在于当前的店面中
        if mealSet:
            TblMealInHouse.objects.filter(house_id = house_id, name=meal_name).update(meal_price = price)
            applyLog.append({'result':'success'})
    return applyLog


def compareMealPrice():
    print('enter compareMealprice')
    flag=1
    house_list = []
    price=[]
    price_list = [] #[{'meal_id':[]}]
    mealSet = TblMeal.objects.all()
    userSet = TblAdminuser.objects.all()
    for item in mealSet:
        for item2 in userSet:
            localMealSet = TblMealInHouse.objects.filter(house_id = item2.house_id,name=item.name)
            if localMealSet:
                for item3 in localMealSet:
                    price.append(item3.meal_price)
                    #price_list[item.name].append(item3.meal_price)
            else:
                #price_list[item.name].append(0)
                price.append(0)
            if flag==1:
                house_list.append(item2.house_name)
        price_list.append({'meal_name':item.name, 'price':price})
        price=[]
        flag=0
    print('house_list:',house_list, 'price_list:', price_list)
    return {'house_list':house_list, 'price_list':price_list}

def getUpdateMealInfo(post):
    mealInfoDict = {}
    category_list = []
    meal_id = post.get('meal_id', None)
    house_id = post.get('house_id', None)
    print('getUpdateMealInfo:', meal_id, 'house_id', house_id)
    mealSet = TblMealInHouse.objects.filter(meal_id = meal_id, house_id=house_id)
    if mealSet:
        for item in mealSet:
            try:
                userSet = TblAdminuser.objects.get(house_id=item.house_id)
                house_name = userSet.getHouseName()
                house_list = [{'house_name':house_name, 'house_id':item.house_id}]
                userSet1 = TblAdminuser.objects.exclude(house_id=item.house_id)
                for item1 in userSet1:
                    house_list.append({'house_name':item1.house_name, 'house_id':item1.house_id})
                cateSet = TblMealCategory.objects.filter(id=item.category_id)
                for item2 in cateSet:
                    category_list = [{'id':item2.id, 'name':item2.name}]
                cateSet1 = TblMealCategory.objects.exclude(id=item.category_id)
                for item3 in cateSet1:
                    category_list.append({'id':item3.id, 'name':item3.name})
            except ObjectDoesNotExist:
                print ('getUpdateMealInfo/get house_name fail')
                return None
            mealInfoDict = {
                'meal_id':meal_id,
                'meal_name': item.name,
                'meal_price':item.meal_price,
                'meal_content':item.detail_content,
                'house_id':item.house_id,
                'house_list':house_list,
                'category_list':category_list,
                #'category_id':item.category_id,
                'avatar_url':item.avatar_url#这里如何获取图片预览？
            }
    else:
        print('there is no such meal in house')
        return None
    print('mealInfoDict:', mealInfoDict)
    return mealInfoDict