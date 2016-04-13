from django.shortcuts import render, render_to_response
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import redirect, Http404
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from DiningMealManage.models import TblAdminuser
import json
from DiningMealManage import cron
from DiningMealManage.models import TblBill
from DiningServer.service import weixin_service, order_service
from DiningServer.common import tpl_msg_data
import sys
import time
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
#在服务器上测试时，需要导入以下三部分模块
from DiningServer.common.time_format_util import *
from DiningServer.common.func import *
from DiningHouse.settings import WC_PAY_MCHID


def loginGuide(request):
    print('enter MealManage-loginGuide')
    return render(request, 'DiningMealManage/single.html')

#退出
def logout(request):
    print ('enter in logout')
    response = HttpResponse({'response':'fail'})
    response.delete_cookie('username')
    response.delete_cookie('type')
    return response

@csrf_exempt
def login(request):
    print ('enter DiningMealManage login')
    if request.method == 'POST':
        print('post:', request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('user_name:',username, 'password:',password)
        try:
            user = TblAdminuser.objects.get(username__exact = username,password__exact = password)
            userType = user.getUserType()
            house_id = user.getHouseId()#add for show del_record
            response = HttpResponseRedirect('/DiningMealManage/pushPage/')
            response.set_cookie('username', username, 3600*12)#假设登录持续时间为12小时
            response.set_cookie('type', userType, 3600*12)
            response.set_cookie('house_id', house_id, 3600*12)
            print ('login/house_id:',house_id)
            return response
        except ObjectDoesNotExist:
            print('非法登录！')
            # return HttpResponse('无当前用户')
            return HttpResponseRedirect('/DiningMealManage/login/')
    else:
        print('redirect to login.html')
        return HttpResponseRedirect('/DiningMealManage/login/')
@csrf_exempt
def pushPage(request):
    print ('enter DiningMealManage-pushPage')
    username = request.COOKIES.get('username','')
    try:
        userSet = TblAdminuser.objects.get(username=username)
        house_name = userSet.getHouseName()
        return render_to_response('DiningMealManage/content.html', {'house_name':house_name})
    except ObjectDoesNotExist:
        print ('pushPage ObjectsDoseNotExist')
        return HttpResponseRedirect('/DiningMealManage/login/')

#定时推送未处理订单到订单管理界面
@csrf_exempt
def schdule_task(request):
    print('enter schdule_task')
    username = request.COOKIES.get('username', )
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        #userType = houseSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        print('schdule_task dose not exist, 请重新登录')
        return HttpResponse('there is no loguser')
    context = cron.schduled_push(local_id)
    # context = {'test':[{'key1':1,'key2':2},{'key1':3,'key2':4},{'key1':5,'key2':6},{'key1':7,'key2':8}]}
    print ('context:', context)
    #return HttpResponse(json.dumps(context, ensure_ascii=False))
    #return render(request, 'DiningMealManage/pushOrder.html', context)
    return render_to_response('DiningMealManage/pushOrder.html', context)

#商家订单处理部分（确认或取消）
@csrf_exempt
def deal_order(request):
    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    print ('enter in deal_order')
    print ('post: ',request.POST)
    username = request.COOKIES.get('username', )
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        house_name = houseSet.getHouseName()
    except ObjectDoesNotExist:
        print('deal_order dose not exist, 请重新登录')
        return HttpResponseRedirect('/DiningMealManage/login/')
    result = cron.updateBillState(local_id, request.POST)
    if sys.platform.startswith('win'):
        print('当前测试平台')
    else:
        #取消订单，通知微信 add by ljz 02-29
        openid = request.POST.get('openid', None)
        flag = request.POST.get('flag', None)
        bill_id = request.POST.get('bill_id', None)
        print('openid', openid, 'flag', flag, 'bill_id', bill_id)

        bill_info = TblBill.objects.filter(id=bill_id)[0]
        bill_add_time = bill_info.add_time

        if flag == '1':#如果是确认订单
            touser = openid
            print('openid:',touser)
            template_id = 'HRECa6Gb9oRqcHS-G7krnT5_bqBsOgYJsKwga52O0xE'
            url = ''

            print('deal_order/确认订单内容：', bill_info.add_time, bill_info.all_fee)
            tpl_msg_data.accept_data['keyword1']['value'] = '家家长沙米粉'+'('+house_name+')'
            tpl_msg_data.accept_data['keyword2']['value'] = bill_add_time.strftime('%Y-%m-%d %H:%M:%S')
            tpl_msg_data.accept_data['keyword3']['value'] = '详情见商家小票'
            tpl_msg_data.accept_data['keyword4']['value'] = str('%.2f' % float(bill_info.all_fee))
            data = tpl_msg_data.accept_data

            weixin_service.sendTplMsg(request, touser, template_id, url, data)
            print('send confirm msg over!!!!!!!!!!!')
        else:#取消订单
            touser = openid
            print('openid:',touser)
            template_id = '6E5y5UZsExW45VywamzEzk7eyf8eOM1KXKSzJyU5NHQ'
            url = ''

            tpl_msg_data.deny_data['keyword1']['value'] = bill_info.id
            tpl_msg_data.deny_data['keyword2']['value'] = bill_add_time.strftime('%Y-%m-%d %H:%M:%S')
            tpl_msg_data.deny_data['keyword3']['value'] = str(time_now)
            data = tpl_msg_data.deny_data
            weixin_service.sendTplMsg(request, touser, template_id, url, data)
            print('send cancel msg over!!!!!!!!!!!')

            print('starting refund...............')
            out_trade_no = str(bill_info.id).replace('-','')
            out_refund_no = out_trade_no

            (yuan,fen) = str('%.2f' % float(bill_info.all_fee)).split('.')
            total_fee = int(yuan)*100 + int(fen)
            refund_fee = total_fee

            op_user_id = WC_PAY_MCHID
            print('out_trade_no:',out_trade_no)
            print('out_refund_no:',out_refund_no)
            print('refund_fee:',refund_fee)
            print('op_user_id:',op_user_id)
            refund_response = weixin_service.refund(request,out_trade_no,out_refund_no,total_fee,refund_fee,op_user_id)
            if refund_response:
                print('finish refund................')
                bill_info.bill_state = order_service.BILL_STATE_REFUND
                bill_info.save()
                #return json_response('已经申请退款，请在三个工作日之后查看银行账户通知')
            else:
                pass
                #return json_response('退款操作失败')
    print('result:', result)
    context = cron.schduled_push(local_id)
    #需要将传递过来的openid给静存，用于微信发送一个确认消息给用户
    return render(request, 'DiningMealManage/pushOrder.html', context)
    #return HttpResponse(json.dumps(context, ensure_ascii=False))

#处理完订单，向订单管理页面中下面的数据显示栏分别插入记录
@csrf_exempt
def insert_order(request):
    print('enter in insert-order')
    print ('post: ',request.POST)
    username = request.COOKIES.get('username', )
    print ('username:', username)
    try:
        houseSet = TblAdminuser.objects.get(username=username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
    except ObjectDoesNotExist:
        print ('enter ObjectDoseNotExit')
        return HttpResponseRedirect('/DiningMealManage/login/')
    context = cron.insert_to_record(local_id, request.POST)
    return render(request, 'DiningMealManage/deal_record.html', context)

@csrf_exempt
def print_order(request):
    print ('enter in print_order')
    context = cron.printOrder(request.POST)
    #return render(request, 'DiningMealManage/Print.html', context)
    print('print_order/context: ', context)
    return render(request, 'DiningMealManage/Print.html', context)


@csrf_exempt
def show_order_detail(request):
    print('enter show_order_detail')
    username = request.COOKIES.get('username', )
    print('post:', request.POST)
    try:
        houseSet = TblAdminuser.objects.get(username = username)#获取本地登录的权限信息
        local_id = houseSet.getHouseId()
        #userType = houseSet.getUserType()#获取当前用户的类型
    except ObjectDoesNotExist:
        print('show_order_detail dose not exist, 请重新登录')
        return HttpResponseRedirect('/DiningMealManage/login/')
    context = cron.getOrderDetails(local_id, request.POST)
    print('show_order_detail/context: ', context)
    # return render_to_response('DiningMealManage/showOrderDetail.html', context)
    return render(request, 'DiningMealManage/showOrderDetail.html', context)


@csrf_exempt
def sure_arrive(request):
    print ('sure_arrive:post: ', request.POST)
    context = cron.orderSure(request.POST)
    print('sure_arrive:', context)
    return HttpResponse(json.dumps(context, ensure_ascii=False))