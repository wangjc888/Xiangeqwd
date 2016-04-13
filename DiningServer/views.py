from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template

from DiningServer.service import meal_service,user_service,order_service,time_service,weixin_service
from DiningHouse.settings import *
from DiningServer.models import *
from DiningServer.common.func import *
from DiningServer.read_excel import startGenerator
from DiningServer.common.time_format_util import *
from DiningServer.common import tpl_msg_data
from uuid import uuid4
import json,pickle
import datetime,time

"""
在这里郑重声明   order = bill =  订单
"""
# Create your views here.
def welcome(request, urls):
	return render(request, 'DiningServer/'+urls+'.html')

def generatorMeals(request):
	"""
	调用service从excl中构造meal
	:param request:
	:return:
	"""
	startGenerator()
	return HttpResponse('success hahahaha')

def getUserFromOpenid(request):
	code = request.GET.get('code',None)
	
	redirect_uri = 'http://xiangeqwd.9xi.com'+request.path
	print('code in %s:'%redirect_uri,code)
	openid = weixin_service.getOpenid(request,redirect_uri)
	print('openid in %s:'%redirect_uri,openid)
	# request.session['openid'] = openid

	if openid and TblUser.objects.filter(openid=openid).count() == 0:
		user = TblUser.objects.create(id=uuid4(),
									add_time=time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time())),
									openid=openid)
	elif openid and TblUser.objects.filter(openid=openid).count() != 0:
		try:
			user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-default','-add_time')[0]
		except:
			user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]
		else:
			user = TblUser.objects.filter(openid=openid).order_by('-add_time')[0]
	else:
		return None
	print('user.openid:',user.openid)
	return user

@csrf_exempt
def index(request):
	"""
	首页
	:param request:
	:return:
	"""

	user = getUserFromOpenid(request)
	if user:
		request.session['openid'] = user.openid
		openid = user.openid
		print('openid(from user) in index:',user.openid) 
	else:
		openid = request.session.get('openid',None)
		print('openid(from session) in index:',openid)    
	
	context = meal_service.getCategoryAndList(request)
	
	# 判断当前是否为营业时间
	now_time = datetime.datetime.now().strftime('%X') 
	print('now_time:',now_time)
	if 'house' in context:
		house_open_time = context['house']['open_time']
		house_close_time = context['house']['close_time']
		
		tpl_msg_data.welcom_data['keyword1']['value'] = '家家长沙米粉'+'('+context['house']['name']+')'

		if now_time < house_open_time.strftime('%X')  or now_time > house_close_time.strftime('%X') :
			return render_to_response('DiningServer/rest.html',{
															'open_time':house_open_time,
															'close_time':house_close_time})

	# touser = request.session['openid']
	# template_id = 'X-1HSV69BTa03E5gj-ySu7sao7_N9Cx9EuLIlZzIYDI'
	# url = ''
	# data = tpl_msg_data.welcom_data
	# weixin_service.sendTplMsg(request, touser, template_id, url, data)

	print('request method:', request.method)
	if 'house' in context:
		request.session['house_id'] = context['house']['house_id']
		print('house_id in session:',request.session['house_id'])
	
	return render(request, 'DiningServer/index.html', context)

@csrf_exempt
def switch(request):
	"""
	更换门店
	:param request:
	:return:
	"""
	# if request.method == 'POST':
	#     house_id = request.POST.get('house_id',None)

	#     return HttpResponseRedirect('/DiningServer/index/?house_id=%s'%house_id)
	# else:
	houselist = TblHouse.objects.all()
	openid = request.session['openid']
	print('openid index2switch:',openid)

	return render_to_response('DiningServer/inBranch.html', {'houselist':houselist,
															'openid':openid,
															},context_instance=RequestContext(request))

def getMealDetail(request):
	"""
	获取商品详情页面
	:param request:
	:param meal_id:
	:return:
	"""
	meal_id = request.GET.get('meal_id',None)
	house_id = request.GET.get('house_id',None)
	print('meal_id:',meal_id)
	print('house_id:',house_id)

	context = meal_service.getMealDetailInHouse(meal_id,house_id)
	for k,v in context.items():
		print(k,v)

	return render(request, 'DiningServer/details.html', context)


"""
个人信息相关
"""
@csrf_exempt
def getMyDetailInfoPage(request):
	"""
	获取我的相信信息接口
	:param request:
	:return:
	"""
	
	# 使用ensure_ascii = False   否则的话中文会只显示编码 不显示汉
	user = getUserFromOpenid(request)
	if user:
		request.session['openid'] = user.openid
		openid = user.openid
		print('openid(from user) in index:',user.openid) 
	else:
		openid = request.session.get('openid',None)
		print('openid(from session) in index:',openid) 


	try:
		user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-default','-add_time')[0]
	except:
		user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]

	return render_to_response("DiningServer/userInfoPage.html", {'user':user},context_instance=RequestContext(request))

@csrf_exempt
def listMyDetailInfoPage(request):
	"""
	获取我的相信信息列表
	:param request:
	:return:
	"""
	user = getUserFromOpenid(request)
	if user:
		request.session['openid'] = user.openid
		openid = user.openid
		print('openid(from user) in index:',user.openid) 
	else:
		openid = request.session.get('openid',None)
		print('openid(from session) in index:',openid) 
	
	if request.method == 'POST':

		method = request.POST.get('method','').strip()
		print('method:',method)
		user_id = request.POST.get('user_id','').strip()
		print('user_id:',user_id)

		if method == 'default':
			print('default in list!!!!!')
			user = TblUser.objects.filter(id=user_id)[0]
			user.default = user_service.SET_DEFAULT
			user.save()

			TblUser.objects.filter(openid=openid).exclude(id=user_id).update(default=user_service.NO_DEFAULT)
			return json_response('success')

		elif method == 'delete':
			print('delete in list!!!!!')
			user = TblUser.objects.filter(id=user_id)[0]
			user.access = user_service.DENY
			user.save()

			return json_response('success')
		elif method == 'edit':
			# return HttpResponseRedirect("/DiningServer/modifyMyDetailInfo/")
			print('edit in list!!!!!')
			user = TblUser.objects.filter(id=user_id)[0]
			user.default = user_service.SET_DEFAULT
			user.save()

			TblUser.objects.filter(openid=openid).exclude(id=user_id).update(default=user_service.NO_DEFAULT)
			return json_response('success')

	userlist = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-default','-add_time')[:3]
	return render_to_response("DiningServer/userInfoPageList.html", {'userlist':userlist},context_instance=RequestContext(request))

@csrf_exempt
def modifyMyDetailInfo(request):
	"""
	修改我的信息 接口
	:param request:
	:return:
	"""

	openid = request.session.get('openid','openiddefault')
	print('openid:',openid)
	time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))

	if request.method == 'POST':
		username = request.POST.get('username','').strip()
		sex      = request.POST.get('sex','1').strip()
		phone    = request.POST.get('phone','').strip()
		add_time = time_now
		region = request.POST.get('region','').strip()
		print('region:',region)
		door = request.POST.get('location','').strip()
		print('door:',door)

		print('degree:',request.POST['degree'])
		YX = request.POST.get('degree','114.0480804443,22.5414180756').strip()
		print('YX:',YX)
		latitude = YX.split(',')[-1].strip()
		print(latitude)
		longitude = YX.split(',')[0].strip()
		print(longitude)

		default = user_service.SET_DEFAULT
		access = user_service.ALLOW
		user_id = request.POST.get('user_id','')
		print('user_id:',user_id)
		# latitude = request.session.get('latitude',float(40))
		# longitude = request.session.get('longitude',float(116))

		if not latitude or not longitude:
			return HttpResponseRedirect("/DiningServer/modifyMyDetailInfo/")

		if not openid:
			openid = request.session.get('openid','openiddefault')
			
		TblUser.objects.filter(id=user_id).update(
													username=username,
													sex=int(sex),
													phone=phone,
													add_time=add_time,
													user_location=region,
													door=door,
													latitude=float(latitude),
													longitude=float(longitude),
													default=default,
													access=access
													)

		TblUser.objects.filter(openid=openid).exclude(id=user_id).update(default=user_service.NO_DEFAULT)

		return HttpResponseRedirect('/DiningServer/listMyDetailInfoPage/')
	else:
		user_id = request.GET.get('user_id','')
		print('user_id:',user_id)

		if not openid:
			openid = request.session.get('openid','')
		print('openid:',openid)

		if not user_id:
			return HttpResponseRedirect("/DiningServer/addMyDetailInfo/")
		try:
			user = TblUser.objects.filter(id=user_id)[0]
		except:
			psss
		return render_to_response("DiningServer/userInfoPage.html", {'user':user},context_instance=RequestContext(request))


@csrf_exempt
def addMyDetailInfo(request):
	"""
	修改我的信息 接口
	:param request:
	:return:
	"""

	openid = request.session.get('openid','openiddefault')
	print('openid:',openid)
	time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))

	if request.method == 'POST':
		username = request.POST.get('username','').strip()
		sex      = request.POST.get('sex','1').strip()
		phone    = request.POST.get('phone','').strip()
		add_time = time_now
		region = request.POST.get('region','').strip()
		print('region:',region)
		door = request.POST.get('location','').strip()
		print('door:',door)

		print('degree:',request.POST['degree'])
		YX = request.POST.get('degree','114.0480804443,22.5414180756').strip()
		print('YX:',YX)
		latitude = YX.split(',')[-1].strip()
		print(latitude)
		longitude = YX.split(',')[0].strip()
		print(longitude)
		default = user_service.SET_DEFAULT
		access = user_service.ALLOW
		user_id = request.POST.get('user_id','')

		if not latitude or not longitude:
			return HttpResponseRedirect("/DiningServer/addMyDetailInfo/")

		if not openid:
			openid = request.session.get('openid','openiddefault')
			
		TblUser.objects.filter(openid=openid).update(default=user_service.NO_DEFAULT)

		tbl_user = TblUser( 
							id = uuid4(),
							openid=openid,
							username=username,
							sex=int(sex),
							phone=phone,
							add_time=add_time,
							user_location=region,
							door=door,
							latitude=float(latitude),
							longitude=float(longitude),
							default=default,
							access=access
							)
		tbl_user.save()

		
		return HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxacfdb1da76aa7763&redirect_uri=http%3A%2F%2Fxiangeqwd.9xi.com%2FDiningServer%2FlistMyDetailInfoPage%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect')
	else:
		return render_to_response("DiningServer/userInfoPageAdd.html", {},context_instance=RequestContext(request))



"""
订单相关页面及接口
"""

@csrf_exempt
@require_POST
def gotoOrderPage(request):
	"""
	点击去下单 跳转到的页面
	:param request:
	:return:
	"""
	openid = request.session.get('openid','openiddefault')
	print('openid in shopping:',openid)
	user = user_service.getMyDetailInfo(openid)
	
	house_id = request.session.get('house_id','houseiddefault')

	bill = order_service.createOrder(request)
	time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
	meals = meal_service.getMealsAndCount(request.POST)

	count = 0
	sum = 0
	buy_meals = meals['meal_list']
	for meal in buy_meals:
		print('meal in buy_meal:\n',meal)
		count += int(meal['buy_count'])
		sum += int(meal['buy_count']) * float(meal['meal_price'])

		# 保存订单中的商品
		bill_meal = TblBillMeal()
		bill_meal.id = uuid4()
		bill_meal.meal_id = meal['meal_id']
		bill_meal.bill_id = bill.id
		bill_meal.house_id = bill.house_id
		bill_meal.openid = bill.openid
		bill_meal.user_id = user['id']

		bill_meal.add_time = time_now
		bill_meal.meal_name = meal['meal_name']
		bill_meal.meal_url = meal['avatar_url']
		bill_meal.meal_price = float(meal['meal_price'])
		bill_meal.buy_count = int(meal['buy_count'])
		bill_meal.save()

		try:
			meal_in_house = TblMealInHouse.objects.filter(house_id=house_id,meal_id=meal['meals_id'])[0]
			meal_in_house.sold_count += int(meal['buy_count'])
			meal_in_house.save()
		except:
			pass

	print("count:",count)
	print("sum:",sum)
	print("bill_id:",bill.id)
	print("order Done!!!")

	delivery_fee = float(0.01)
	# delivery_fee = order_service.getDeliveryFee(request, sum)
	total_fee = sum + delivery_fee
	times = time_service.getTimeOption()

	context = {'meals':meals, 'user':user, 'times': times, 'count': count, 'sum':sum, 'delivery_fee':delivery_fee, 'total_fee':total_fee, 'bill_id':bill.id}

	# touser = openid
	# template_id = 'HRECa6Gb9oRqcHS-G7krnT5_bqBsOgYJsKwga52O0xE'
	# url = ''

	# tpl_msg_data.accept_data['keyword1']['value'] = '家家长沙米粉'
	# tpl_msg_data.accept_data['keyword2']['value'] = str(time_now)
	# tpl_msg_data.accept_data['keyword3']['value'] = '详情见商家小票'
	# tpl_msg_data.accept_data['keyword4']['value'] = all_fee
	# data = tpl_msg_data.accept_data

	# weixin_service.sendTplMsg(request, touser, template_id, url, data)

	return render(request, 'DiningServer/shopping.html', context)

# 创建订单 创建完成后自动跳转到支付页面
@csrf_exempt
def createOrder(request):
	"""
	创建订单接口
	:param request:
	:return:
	"""
	openid = request.session.get('openid','openiddefault')
	user = user_service.getMyDetailInfo(openid)

	if not user['username'] or not user['phone'] or not user['user_location']:
		return HttpResponseRedirect("/DiningServer/modifyMyDetailInfo/")

	if request.method == 'GET':
		bill_id = request.GET.get('bill_id',None)
		sum = request.GET.get('sum',None)
	else:
		bill_id = request.POST.get('bill_id',None)
		sum = request.POST.get('sum',None)
	
	print('bill_id in create:',bill_id)
	print('sum in create:',sum)
	try:
		bill = TblBill.objects.filter(id=bill_id)[0]
	except:
		return render_to_response('DiningServer/404.html')

	if request.method == 'POST':
		print('POST send_time:',request.POST.get('send_time',''))
		# bill.bill_content = request.POST.get('remarks','')
		bill.ensure_send_time = request.POST.get('send_time','')
		bill.save()
		
	# (yuan,fen) = str('%.2f' % float(sum)).split('.')
	(yuan,fen) = str('%.2f' % float(bill.all_fee)).split('.')
	print(yuan,fen)

	body = 'Xiangeqing WeiDao'    #'家家长沙米粉'.encode('utf-8','xmlcharrefreplace').decode('latin1')
	out_trade_no = str(bill_id).replace('-','')
	total_fee = int(yuan)*100 + int(fen)
	spbill_create_ip = request.META.get('REMOTE_ADDR', "120.25.151.185")
	notify_url = 'http://xiangeqwd.9xi.com/notifyPay/'

	openid = request.session.get('openid','openiddefault')
	print('openid in createOrder:',openid)
	pay_response = weixin_service.callOrderAPI(request,body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid)
	try:
		prepay_id = pay_response.get('prepay_id','')
	except:
		prepay_id = 'wx201603021557412c3168e0b20043476737'
	js_params = weixin_service.genJsAPIParams(prepay_id)

	TblBill.objects.filter(id=bill_id).update(prepay_id=prepay_id)

	context = {
			'bill_id':bill_id,
			'sum':sum,
			'all_fee':bill.all_fee,

			'prepay_id':prepay_id,
			'appId':WC_PAY_APPID,
			'openid':openid,
			'nonceStr':js_params.get('nonceStr',''),
			'timeStamp':js_params.get('timeStamp',''),
			'package':"prepay_id=%s" % prepay_id,
			'signType':js_params.get('signType',''),
			'paySign':js_params.get('paySign',''),
			}

	return render_to_response("DiningServer/createOrder.html", context,context_instance=RequestContext(request))

@csrf_exempt
def notifyPay(request):
	"""
	支付成功后微信回调地址
	"""
	xml_msg = '<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>'
	return HttpResponse(xml_msg)
			
@csrf_exempt
def getOrder(request):
	"""
	支付完成饭后跳转到用户订单页面
	:param request:
	:return: 返回”我的订单页面“
	"""
	print('method:',request.method)
	openid = request.session.get('openid','openiddefault')
	print('openid in getOrders:',openid)

	bill_id = request.GET.get('bill_id',None)
	print('bill_id in getOrder:',bill_id)

	out_trade_no = str(bill_id).replace('-','')
	pay_result = weixin_service.callQueryPayResult(out_trade_no)
	print('pay_result:',pay_result)

	order_service.payOrder(request,bill_id,pay_result)
	try:
		bill = TblBill.objects.filter(id=bill_id)[0]
	except:
		return render_to_response('DiningServer/404.html')

	myMeals = TblBillMeal.objects.filter(bill_id=bill_id)
	
	try:
		user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-default','-add_time')[0]
	except:
		user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]
		
	print('len(myMeals):',len(myMeals))

	return render_to_response("DiningServer/myOrder.html", {'bill':bill,
															'myMeals':myMeals,
															'user':user,
															},context_instance=RequestContext(request))



@csrf_exempt
def getOrdersByType(request):
	"""
	获取用户订单
	:param request: httprequest
	:return: 渲染后的订单列表
	"""
	user = getUserFromOpenid(request)
	if user:
		request.session['openid'] = user.openid
		openid = user.openid
		print('openid(from user) in index:',user.openid) 
	else:
		openid = request.session.get('openid',None)
		print('openid(from session) in index:',openid) 

	if request.method == 'POST':
		bill_id = request.POST.get('bill_id').strip()
		method = request.POST.get('method').strip()
		if method == 'delete':
			print('bill_id in order delete:',bill_id)
			TblBill.objects.filter(id=bill_id).update(access=order_service.DENY)

	context = order_service.getMyBills(openid)
	for k,v in context.items():
		print(k,v)
	return render(request, 'DiningServer/allOrder.html', context)



@csrf_exempt
def getBillDetail(request):
	"""
	我的订单中进入订单详情
	:param request:
	:return:
	"""
	# openid = request.session.get('openid','openiddefault')
	bill_id = request.GET.get('bill_id','')

	print('bill_id in bill deatails:',bill_id)
	try:
		bill = TblBill.objects.filter(id=bill_id)[0]
		user = TblUser.objects.filter(id=bill.user_id)[0]
		myMeals = TblBillMeal.objects.filter(bill_id=bill_id)
	except:
		return render_to_response('DiningServer/404.html')

	return render_to_response("DiningServer/billDetails.html", {'bill':bill,
																'user':user,
																'myMeals':myMeals,
															},context_instance=RequestContext(request))




@csrf_exempt
def ensureSend(request):
	"""
	确认送达 接口
	:param request:
	:return:
	"""
	# order_service.ensureSend(bill_id)
	bill_id = request.GET.get('bill_id',None)
	print('bill_id in ensureSend:',bill_id)
	bill = TblBill.objects.filter(id=bill_id)[0]

	if bill.bill_state != order_service.BILL_STATE_SENDING:
		return False

	# 更改状态为待评价
	bill.bill_state = order_service.BILL_STATE_JUDGE
	bill.ensure_send_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
	bill.save()

	return None


"""
评价订单以及获取评价等页面
"""
@csrf_exempt
def judgeMeal(request):
	"""
	评价商品
	:param request:
	:return:
	"""

	if request.method == 'POST':
		
		try:
			bill_id = request.POST.get('bill_id',None)
			bill = TblBill.objects.filter(id=bill_id)[0]
		except:
			return render_to_response('DiningServer/404.html')
		print('bill_id:',bill_id)

		judge_meal    = request.POST.get('judge_meal',None)
		judge_speed   = request.POST.get('judge_speed',None)
		judge_message = request.POST.get('judge_message',None)
		print('judge_meal:',judge_meal)
		print('judge_speed:',judge_speed)
		print('judge_message:',judge_message)

		tbl_bill_meal = TblBillMeal.objects.filter(bill_id=bill_id)
		for meal in tbl_bill_meal:
			tbl_judge_meal = TblJudgeMeal(
										id=uuid4(),
										house_id=bill.house_id,
										bill_id=bill_id,
										meal_id=meal.meal_id,
										user_id=bill.user_id,
										judge_meal=judge_meal,
										judge_speed=judge_speed,
										judge_message=judge_message,
										add_time=time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time())),
										)
			tbl_judge_meal.save()

		bill.bill_state = order_service.BILL_STATE_JUDGED
		bill.save()

		print('json_response:',json_response('success'))
		return json_response('success')
		# return HttpResponseRedirect("/DiningServer/getHouseJudge/?house_id=%s" % bill.house_id)
	else:
		try:
			bill_id = request.GET.get('bill_id',None)
		except:
			return render_to_response('DiningServer/404.html')

		context = order_service.getBillDetail(bill_id)
		for k,v in context.items():
			print(k,v)
		return render(request, 'DiningServer/comoder.html', context)


@csrf_exempt
def getMealJudge(request):
	"""
	获取商品评价界面
	:param request:
	:return:
	"""
	try:
		bill_id = request.GET.get('bill_id',None)
		print('bill_id in getMealJudge:',bill_id)
		mealJudge = TblJudgeMeal.objects.filter(bill_id=bill_id)[0]
	except:
		return render_to_response('DiningServer/404.html')
	return render_to_response("DiningServer/comoderview.html", {'mealJudge':mealJudge},context_instance=RequestContext(request))

@csrf_exempt
def getHouseJudge(request):
	"""
	获取店面评价界面
	:param request:
	:return:
	"""
	
	try:
		house_id = request.GET.get('house_id',None)
		print('house_id in getHouseJudge:',house_id)
		context = order_service.getHouseJudgeSet(house_id)
		for k,v in context.items():
			print(k,v)
	except:
		return render_to_response('DiningServer/404.html')
	context = order_service.getHouseJudgeSet(house_id)
	return render(request, 'DiningServer/evaluate.html', context)


def refund(request):
	"""
	申请退款
	:param request:
	:return:
	"""
	bill_id = request.POST.get('bill_id', None)
	try:
		bill = TblBill.objects.filter(id=bill_id)[0]
	except:
		return render_to_response('DiningServer/404.html')

	if bill.bill_state != order_service.BILL_STATE_PAY:
		return json_response('商家只能在取消订单时进行退款')

	out_trade_no = str(bill_id).replace('-','')
	out_refund_no = out_trade_no

	(yuan,fen) = str('%.2f' % float(bill.all_fee)).split('.')
	total_fee = int(yuan)*100 + int(fen)
	refund_fee = total_fee

	op_user_id = WC_PAY_MCHID

	refund_response = weixin_service.refund(request,out_trade_no,out_refund_no,total_fee,refund_fee,op_user_id)
	if refund_response:
		bill.bill_state = order_service.BILL_STATE_REFUND
		bill.save()

		return json_response('已经申请退款，请在三个工作日之后查看银行账户通知')
	else: 
		return json_response('退款操作失败')


def refundQuery(request):
	"""
	退款结果查询
	:param request:
	:return:
	"""
	bill_id = request.GET.get('bill_id', None)
	out_trade_no = str(bill_id).replace('-','')

	refundQuery_response = weixin_service.refundQuery(request,out_trade_no)
	if refundQuery_response:
		return json_response('退款成功')
	else: 
		return json_response('退款正在进行中')


from wechat_sdk.basic import WechatBasic
from django.http.response import HttpResponseBadRequest
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import LocationMessage
from wechat_sdk.context.framework.django import DatabaseContextStore

@csrf_exempt
def getToken(request):
	token = 'xiangeqwd'
	wechat = WechatBasic(token=token)  

	if wechat.check_signature(signature=request.GET.get('signature',''),
							  timestamp=request.GET.get('timestamp',''),
							  nonce=request.GET.get('nonce','')):
		# return HttpResponse(request.GET.get('echostr', 'error'))
		print('request method in getToken:',request.method)

		if request.method == 'GET':
			response = request.GET.get('echostr', 'error')
		else:
			xml2dict = wechat.parse_data(request.body)

			for k,v in xml2dict.items():
				print(k,v)

			if xml2dict['Event'] == 'LOCATION' or 'VIEW':
				# if 'FromUserName' not in xml2dict or not xml2dict['FromUserName']:
				# 	xml2dict['FromUserName'] = request.META.get('REMOTE_ADDR')

				if 'Latitude' not in xml2dict.keys() or 'Longitude' not in xml2dict.keys():
					latitude = float(22.5414180756)
					longitude = float(114.0480804443)
				else:
					latitude = float(xml2dict['Latitude'])
					longitude = float(xml2dict['Longitude'])

				# if not TblUser.objects.filter(openid=xml2dict['FromUserName']):
				# 	user = TblUser.objects.create(
				# 		id=uuid4(),
				# 		add_time=time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time())),
				# 		openid=xml2dict['FromUserName']
				# 		)

				if TblUser.objects.filter(openid=xml2dict['FromUserName']).count() == 0:
					tbl_user = TblUser(
									id=uuid4(),
									add_time=time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time())),
									openid=xml2dict['FromUserName'],
									latitude=latitude,
									longitude=longitude,
									default=user_service.SET_DEFAULT,
									access=user_service.ALLOW)
					tbl_user.save()
				# else:
				# 	TblUser.objects.filter(openid=xml2dict['FromUserName']).update(
				# 		latitude=latitude,
				# 		longitude=longitude)

				request.session['openid'] = xml2dict['FromUserName']
			# message = wechat.get_message()
			# response = wechat.response_text(u'消息类型: {}'.format(message.type))
			response = 'success'
	else:
		return HttpResponseBadRequest('Verify Failed')
	return HttpResponse(response)

# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxacfdb1da76aa7763&redirect_uri=http%3A%2F%2xiangeqwd.9xi.com%2FDiningServer%2Findex%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect

@csrf_exempt
def createMenu(request):
	
	wechat = WechatBasic(appid='wxacfdb1da76aa7763', appsecret='0f0f71dbff7dbde3e3b07897ddd8f78b')
	wechat.create_menu(
		{
		'button':[
			{
				'type': 'view',
				'name': '家家订餐',
				'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxacfdb1da76aa7763&redirect_uri=http%3A%2F%2Fxiangeqwd.9xi.com%2FDiningServer%2Findex%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
			},
			{
				'type': 'view',
				'name': '送餐信息',
				'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxacfdb1da76aa7763&redirect_uri=http%3A%2F%2Fxiangeqwd.9xi.com%2FDiningServer%2FlistMyDetailInfoPage%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
			},
			{
				'type': 'view',
				'name': '我的订单',
				'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxacfdb1da76aa7763&redirect_uri=http%3A%2F%2Fxiangeqwd.9xi.com%2FDiningServer%2FgetOrdersByType%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
			},
				]
		}
	
	)

