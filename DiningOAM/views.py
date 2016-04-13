from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from DiningServer.service import time_service

from DiningOAM.service import user_service
from DiningOAM.service import order_service
from DiningOAM.service import meal_service
from DiningOAM.service import house_service
from DiningOAM.service import judge_service
from DiningOAM.service import load_service
from DiningHouse import settings
#import django

#import simplejson as json
# Create your views here.
import json

#=========================================
# from DiningOAM.myAcountCheck import MyCustomBackend
# from DiningOAM.models import myAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, Http404
from django.http.response import HttpResponseRedirect

#=========================================
from django.contrib import auth
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django import forms
from DiningOAM.models import TblAdminuser
from DiningOAM.models import TblMealCategory
from django.core.exceptions import ObjectDoesNotExist
from uuid import uuid4#动态生成菜品图片名称
import xlwt
"""
这里是外卖餐厅OAM后台
"""
def loginGuide(request):
    print('enter loginGuide')
    return render(request, 'DiningOAM/login.html')

#注册
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            TblAdminuser.objects.create(username= username,password=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
    return render_to_response('DiningOAM/regist.html',{'uf':uf}, context_instance=RequestContext(request))

def index(request):
    print ('enter index')
    username = request.COOKIES.get('username','')
    print ('username in cookies:', username)
    if username:
        return render_to_response('DiningOAM/index.html', {'username':username})
        # return render(request, 'DiningOAM/index.html')
    else:
        return HttpResponseRedirect('/DiningOAM/login/')
        # raise Http404

#退出
def logout(request):
    response = HttpResponse({'response':'fail'})
    response.delete_cookie('username')
    response.delete_cookie('type')
    return response

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print('post:', request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('user_name:',username, 'password:',password)
        try:
            user = TblAdminuser.objects.get(username__exact = username,password__exact = password)
            userType = user.getUserType()
        except ObjectDoesNotExist:
            user = 0
        # user = TblAdminuser.objects.filter(username__exact = username,password__exact = password)
        # house_name = user.getHouseName()
        if user:
            print('login success: userType:', userType)
            response = HttpResponseRedirect('/DiningOAM/index/')
            response.set_cookie('username', username, 3600)
            response.set_cookie('type', userType, 3600)
            # response.set_cookie('house_name', house_name, 3600)
            return response
        else:
            print('非法登录！')
            return HttpResponseRedirect('/DiningOAM/login/')
    else:
        print('redirect to login.html')
        return HttpResponseRedirect('/DiningOAM/login/')

# @csrf_exempt
# def index(request):
#     # return HttpResponse('index')
#     print('enter in index')
#     # if request.user.is_authenticated == True:
#     return render(request, 'DiningOAM/index.html')
#     # else:
#     #   return HttpResponseRedirect('/DiningOAM/login/')
#

"""
用户接口部分
"""
@csrf_exempt
def getUserAllCountInfo(request):
    print('getUserAllCountInfo===============')
    context = user_service.userAllCountInfo(request.POST)
    #show_count_info = {'show_date_list':['2015-12-23','2015-12-24', '2015-12-25'], 'daliy_cnt_list':[12, 48, 45], 'total_cnt_list':[12, 60, 105]}
    return HttpResponse(json.dumps(context, ensure_ascii=False))


#需要提供时间范围,最后传递至js
@csrf_exempt
@require_POST
def getUserNumber(request):
    """
    获取用户数量
    :param request: http request
    :return: 显示用户数量的json
    """
    #获取数据库中总的用户数量
    print('getUserNumber', request.POST, 'end of print')
    context = user_service.userNumber(request.POST)
    #return render(request, 'DiningOAM/userCount.html', context)
    return render(request, 'DiningOAM/index.html', context)

def getUserCount(request):
    """
    获取用户统计数量
    :param request:
    :return: 每日用户关注数量
    """
    print('getUserCount', request.POST)
    context = user_service.userCount(request.POST)
    return render(request, 'DiningOAM/userCount.html', context)

"""
订单接口部分
"""
@csrf_exempt
def getOrderCount(request):
    """
    获取订单统计
    :param request: http request
    :return: 用户订单统计的json结果
    """
    print('getOrderCount')
    context = order_service.orderCount(request.POST)
    #order_count = {'date_list':['2015-12-25', '2015-12-26','2015-12-27','2015-12-28'], 'count_list':[12, 16, 22, 38]}
    return HttpResponse(json.dumps(context, ensure_ascii=False))
    #return render(request, 'DiningOAM/orderCal.html', context)

@csrf_exempt
def getOrderList(request):
    """
    获取订单列表
    :param request:
    :return:
    """
    print('enter getOrderList')
    print('getOrderList:', request.POST)
    username = request.COOKIES.get('username', )#获取当前的登录用户名
    context = order_service.orderList(username, request.POST)
    print('context:', context)
    return render(request, 'DiningOAM/getOrderList.html', context)
    #return HttpResponse('')

"""
餐品接口部分
"""

@csrf_exempt
#def getMealList(request, house_id):#这里的id为house_id，后添加部分
def getMealList(request):
    """
    获取已经录入的餐品列表
    :param request:
    :return:
    """
    print('enter getMealList!', request.POST)
    # house_id = 1            #   for test 可能为用户在网页下拉选择传给后台，或者正则表达式
    username = request.COOKIES.get('username',)
    # local_user = TblAdminuser.objects.get(username=username)
    # print('house_name:', local_user.getHouseName())
    context = meal_service.mealList(username, request.POST)
    return render(request, 'DiningOAM/getMealList.html', context)

@csrf_exempt
def getUpdateMeal(request):
    print('enter in getUpdateMeal')
    print('post:', request.POST)
    context = meal_service.getUpdateMealInfo(request.POST)
    return render(request, 'DiningOAM/mealPreview.html', context)

# @require_POST
# def updateMealInfo(request):#暂弃用
#     """
#     更新餐品信息 包括餐品的显示顺序
#     :param request:
#     :return:
#     """
#     mealInfo = meal_service.getUpdateInfo(request.POST)
#     context = meal_service.updateMeal(mealInfo)
#     #return render(request, 'DiningOAM/updateMeal.html', context)
#     #return HttpResponse('context')
#     return render(request, 'DiningOAM/mealPreview.html', context)

@require_POST
@csrf_exempt
def addMeal(request):
    """
    新增餐品
    :param request:
    :return:
    """
    print ('enter view.py/addMeal', request.POST)
    # mealInfo = meal_service.getUpdateInfo(request.POST)
    username = request.COOKIES.get('username','')
    print('addMeal username:', username)
    userinfo = TblAdminuser.objects.filter(username=username)
    for item in userinfo:
        print('enter view.pu/addMeal: userinfo:', item.house_name)
        if item.house_name:
            pic_url = uploadPic(request)
            #pic_url = settings.MEDIA_URL+rel_url#保存图片的绝对路径
            print('addMeal/pic_url:', pic_url)
            #context = meal_service.addNewMeal(item.house_id, request.POST)
            context = meal_service.addNewMeal(pic_url, item.house_id, request.POST)
            print('context:', context)
            return HttpResponseRedirect('/DiningOAM/index')#重定向到index页面（初始化）
            #return render_to_response('DiningOAM/index.html', {})
            #return HttpResponseRedirect('/DiningOAM/getMealList/')
            #return HttpResponse(json.dumps(context, ensure_ascii=False))
            # return render(request, 'DiningOAM/mealManage.html', context)
            # if context:
            #     return render(request, 'DiningOAM/prevAddInfo.html', context)
            # else:
            #     return HttpResponse('菜品信息重复，请重新输入')
    else:
        return None



#这里对应的是直接从base库里导入全部的菜品信息
@csrf_exempt
def copyMeal(request):
    print('enter view.py/copyMeal')
    if request.method == 'POST':
        username = request.COOKIES.get('username','')
        try:
            houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
            local_id = houseSet.getHouseId()
            #userType = houseSet.getUserType()#获取当前用户的类型
        except ObjectDoesNotExist:
            context = {'result':'fail', 'atach_info':'当前店面不存在'}
            return HttpResponse(json.dumps(context, ensure_ascii=False))
            #return HttpResponse('there is no loguser')
        context = meal_service.copyBaseMeal(local_id, request.POST)#需要传入当前店面的id
        #if context:
        #    return HttpResponse('从库中导入菜品数据成功')#从超级管理员处复制成功，可以返回导入数据的条数
        #else:
        #    return HttpResponse('从库中个导入数据失败，请重试')
    else:
        context = {'result':'fail', 'atach_info':'访问类型错误'}
    return HttpResponse(json.dumps(context, ensure_ascii=False))


"""
商铺（分店位置）接口部分
"""
@csrf_exempt
def getHouses(request):#获取分店的id
    """
    #获取所有已经录入的分店位置
    获取所有已经录入的分店信息，列表输出
    :param request:
    :return:
    """
    if request.method == 'POST':
        min = request.POST.get('min', 1)
        max = request.POST.get('max', 1)
        print('the date:post', request.POST)
    elif request.method == 'GET':
        min = request.GET.get('min', 2)
        max = request.GET.get('max', 2)
        print('the date:get', request.GET)
    print('enter gethouse!!!!!')
    context = house_service.getHouseInfo()
    # return HttpResponse('context')
    # if min == 1 and max == 1:#默认没有时间输出
    return render(request, 'DiningOAM/getHouseInfoList.html', context)
    # else:
        # return HttpResponse(json.dumps(context, ensure_ascii=False))




@csrf_exempt
@require_POST
def addHouse(request):
    """
    添加分店
    :param request:
    :return:
    """

    print('addHouseInfo============================', request.POST)
    print ('house_name', request.POST.get('house_name'))
    context = house_service.addHouseInfo(request.POST)
    print('view.py/addHouse:', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))
    # return render(request, 'DiningOAM/getHouseInfoList.html', context)
    #for test
    # houseInfo = {'house_name':'维达',
    #              'house_address': '中山北路',
    #              'phone':'123-456',
    #              'gps_info': '123.45,234.56',
    #              'logname': 'weida',
    #              'password':'123',
    #              'type': '超级管理员',
    #              'flag': 1
    #              }
    # return HttpResponse(json.dumps(houseInfo, ensure_ascii=False))
    # return render(request, 'DiningOAM/housePreview.html', {'houseInfo':houseInfo})

@require_POST
def updateHouseInfo(request):
    """
    更新分店信息
    :param request:
    :return:
    """
    houseInfo = house_service.getNewHouseInfo(request.POST)
    context = house_service.updateInfo(houseInfo)
    #return HttpResponse('context')          #更新成功返回一个提示
    return render(request, 'DiningOAM/housePreview.html', context)


"""
获取评分 相关接口
"""
@csrf_exempt
#def getAllJudge(request, house_id):#当前id分店只可以获取本分店的订单的全部评价
def getAllJudge(request):
    """
    获取全部评分
    :param request:
    :return:
    """
    print('enter getAllJudge')
    print ('request:', request.POST)
    username = request.COOKIES.get('username',)
    context = judge_service.getJudgeInfo(username, request.POST)
    return  render(request, 'DiningOAM/getJudgeList.html', context)

@csrf_exempt
# def getJudgeDistribute(request, house_id):#获取当前分店所有的菜品评价信息
def getJudgeDistribute(request):#获取当前分店所有的菜品评价信息
    """
    获取评分的分布
    :return:
    """
    print('enter getJudgeDistribute')
    username = request.COOKIES.get('username', )
    context = judge_service.judgeDistribute(username, request.POST)
    #judgeDistribution = {'judge_service':[123,234,345,456,789], 'judge_meal': [234,123,123,345,678], 'judge_speed':[10, 131, 232, 431, 21]}
    # return render(request, 'DiningOAM/getJudgeList.html', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))

#导出用户评价数据
def loadJudge(request):
    print('enter loadJudge')
    print ('request:', request.POST)
    username = request.COOKIES.get('username', )#当前登录的用户名
    context = load_service.loadJudgeAsExcel(username, request.POST)
    return HttpResponse(json.dumps(context, ensure_ascii=False))
    # return HttpResponse('导出数据成功')


#删除评价信息
@csrf_exempt
def delJudge(request):
    print('enter del judge!!!')
    username = request.COOKIES.get('username', )
    context = judge_service.delJudgeInfo(username, request.POST)
    print('context:', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))#返回添加的结果（同注册）
    # if context:
    #     return render(request, 'DiningOAM/getJudgeList.html', context)

#删除店面信息
@csrf_exempt
def delHouse(request):
    print('enter del house!!!')
    username = request.COOKIES.get('username', )
    toDelId = request.POST.get('id', '1234')
    context = house_service.delHouseInfo(username, toDelId)
    print('context:', context)
    if context:
        return render(request, 'DiningOAM/getHouseInfoList.html', context)

#删除菜品信息
@csrf_exempt
def delMeal(request):
    print('enter del Meal!!!')
    username = request.COOKIES.get('username', )
    # toDelId = request.POST.get('id', '1234')
    # print('getId:', toDelId)
    context = meal_service.delMealInfo(username, request.POST)
    print('context:', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))#返回添加的结果（同注册）
    # if context:
    #     return render(request, 'DiningOAM/getMealList.html', context)

#删除订单信息
@csrf_exempt
def delOrder(request):
    print('enter del order!!!')
    username = request.COOKIES.get('username', )
    toDelId = request.POST.get('id', '1234')
    print('getId:', toDelId)
    context = order_service.delOrderInfo(username, toDelId)
    print('context:', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))

    # if context:
    #     return render(request, 'DiningOAM/getOrderList.html', context)

#这里对应的是直接从base库里导入全部的菜品信息
@csrf_exempt
def getMealAndPrice(request):
    print('enter view.py/getMealAndPrice')
    username = request.COOKIES.get('username', )
    userList = []
    context = {}
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        userType = houseSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        return HttpResponse('there is no loguser')

    if userType:
        userSet = TblAdminuser.objects.all()
        for item in userSet:
            userList.append(item.house_name)    #如果是超级管理员用户，则需要返回所有店面信息
        context = {'house_name': userList}
    #如果是普通管理员，则直接返回当前id菜品列表，当前价格，与价格表中所有价格
    context.update(meal_service.getMealAndPrice(local_id))
    #context = meal_service.getMealAndPrice(local_id)
    return render(request, 'DiningOAM/modifyMealPrice.html', context)
    # return HttpResponse(json.dumps(context, ensure_ascii=False))

@csrf_exempt
def modifyPrice(request):
    print('enter modifyPrice')
    print('post:', request.POST)
    # return HttpResponse('success')
    username = request.COOKIES.get('username', )
    context = {}
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        userType = houseSet.getUserType()#获取当前用户的类型
        local_name = houseSet.getHouseName()
    except ObjectDoesNotExist:
        return HttpResponse('there is no loguser')
    if userType:#如果是超级管理员,且有创建新的价格
        context = meal_service.addNewPrice(local_id, request.POST)#创建新价格
    else:
        context = meal_service.updatePrice(local_id,local_name, request.POST)#用选定的价格更新菜品当前的价格
    return HttpResponse(json.dumps(context, ensure_ascii=False))#返回添加的结果（同注册）

@csrf_exempt
def getStatement(request):#获取所有统计信息
    """
    获取评分的分布
    :return:
    """
    print('enter getStatement')
    username = request.COOKIES.get('username', )
    # context = load_service.createStatement()
    context = {'house_name':['家家1', '家家2', '家家3','家家4', '家家5', '家家6','家家7','家家8', '家家9','家家10','家家11', '家家12','家家13','家家14'],'total_amount':[ 999.8,567.8,234.5,234,123.4,123.1, 45.6, 44, 32,18,17,17,17,17], 'total_sold_cnt':[111,112,113,99,342,123,456,243,245,675,456,245,675,456], 'popular_meal':[], 'total_judge':[]}
    return HttpResponse(json.dumps(context, ensure_ascii=False))

@csrf_exempt
def comparePrice(request):#获取比较信息
    print('enter comparePrice')
    context = meal_service.compareMealPrice()
    return render(request, 'DiningOAM/comparePrice.html', context)
    #return HttpRequest('enter comparePrice')


# from DiningOAM.upload import ImageUploadForm
from PIL import Image
import sys
import random
import string
@csrf_exempt
def uploadPic(request):
    print('enter uploadPic')
    reqfile = request.FILES['picfile']#picfile要和html里面一致
    print('pic:type: ', type(reqfile))
    img = Image.open(reqfile)
    #img.thumbnail((500,500),Image.ANTIALIAS)#对图片进行等比缩放
    name=''.join(random.sample(string.ascii_letters+string.digits, 8))#随机生成8位字符做图片名称
    meal_name = name+'.png'
    print('meal_name:',meal_name)
    #test_rel_path = settings.MEDIA_ROOT+'/'+meal_name
    #test_abs_path = settings.MEDIA_URL+test_rel_path[1:]#多1个'/'需要去掉
    #print('test_abs_path:', test_abs_path)
    # return HttpResponse('test')
    #img.save(settings.MEDIA_ROOT+"/b.png","png")#
    if sys.platform.startswith('win'):
        rel_path = 'DiningOAM/media/'+ meal_name
        img.save(rel_path ,"png")#保存图片到本地路径
        abs_path = rel_path
        #img.save("DiningOAM/media/a.png" ,"png")#保存图片到本地路径
    else:
        rel_path = settings.MEDIA_ROOT+'/'+meal_name
        img.save(rel_path ,"png")
        abs_path = settings.MEDIA_URL+rel_path[1:]#多1个'/'需要去掉
        #img.save("/path/to/media/a.png" ,"png")#
    print ('abs_path:', abs_path)
    return abs_path
    #return rel_path     #返回保存图片的路径

@csrf_exempt
def getCreateMeal(request):
    print('enter getCreateMeal===')
    house_list = []
    category_list=[]
    userSet = TblAdminuser.objects.all()
    category = TblMealCategory.objects.all()
    for item in userSet:
        house_list.append(item.house_name)
    for item2 in category:
        category_list.append({'name':item2.name, 'id':item2.id})
    context = {'house_list':house_list, 'category_list':category_list}
    print('getCreateMeal:context: ',context)
    return render(request, 'DiningOAM/enterCreateMeal.html', context)
# def test(request):
#     print('enter test!======')
#     return render(request, 'DiningOAM/test.html')

@csrf_exempt
def getUpdateHouse(request):#获取待更新的店面信息
    print('enter getUpdateHouse')
    print('post:', request.POST)
    context = house_service.getUpdateHouseInfo(request.POST)
    return render(request, 'DiningOAM/housePreview.html', context)

@csrf_exempt
def updateMeal(request):
    print('enter in updateMeal')
    print('post:', request.POST)
    #reqfile = request.FILES['picfile', None]#picfile要和html里面一致
    reqfile = request.FILES.get('picfile', None)#picfile要和html里面一致
    print('reqfile', reqfile)
    if reqfile == None:
        pic_url = None
    else:
        pic_url = uploadPic(request)
    print('update/pic_url:', pic_url)
    context = meal_service.updateMealInfo(pic_url, request.POST)
    print('context:', context)
    return HttpResponseRedirect('/DiningOAM/index')#重定向到index页面（初始化）
    #return HttpResponse(json.dumps(context, ensure_ascii=False))