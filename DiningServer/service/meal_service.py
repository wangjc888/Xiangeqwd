from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response

from DiningServer.models import *
from DiningServer.service import user_service
from DiningServer.cache import server_cache
from DiningServer import interface
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from uuid import uuid4
import time,datetime
"""
该服务用于获取跟餐品相关的内容
餐品分类、某分店的商品列表、商品详情等
"""

_in_use_ = 1

(MEAL_HIDE,MEAL_SHOW)=range(2)
meal_status = [
			(MEAL_HIDE,'下架'),
			(MEAL_SHOW,'上架'),
			]


def getCategoryAndList(request):
	# 需要返回的数据  商店 banner 分类 第一个分类的餐品
	category_and_meal = interface.CategoryAndMeal()
	#获取菜品分类列表
	#使用缓存
	category_list = []
	# 如果分类数据存在于缓存中 则读缓存
	if server_cache.cache_meal_category:
		print('start get from cache')
		for item in server_cache.cache_meal_category:
			category_list.append(item.id)
			category_and_meal.add_category_and_meals(item.name,item.id)
	# 从数据库中读取 分类数据并存入缓存数据
	else:
		result_list = TblMealCategory.objects.all().order_by('show_order')
		for item in result_list:
			category_list.append(item.id)
			category_and_meal.add_category_and_meals(item.name,item.id)
			#add to cache
			server_cache.cache_meal_category.append(item)

	#判断获取的结果
	if not category_list:
		return '{}'

	#banner
	#从缓存中读取banner数据
	if server_cache.cache_banner:
		for item in server_cache.cache_banner:
			category_and_meal.add_banner(item.banner_url, item.link_url)
	else:
		result_list = TblBanner.objects.filter(in_use=_in_use_).order_by('show_order')
		for item in result_list:
			category_and_meal.add_banner(item.banner_url, item.link_url)
			# add to cache
			server_cache.cache_banner.append(item)


	#判断得出需要获取的最近分店
	openid = request.session.get('openid','openiddefault')
	print('openid in meal_service:',openid)
	try:
		user = TblUser.objects.filter(openid=openid,default=user_service.SET_DEFAULT,access=user_service.ALLOW).order_by('-add_time')[0]
	except:
		try:
			user = TblUser.objects.filter(openid=openid,access=user_service.ALLOW).order_by('-add_time')[0]
		except:
			return render_to_response('DiningServer/404.html')

	print('user.latitude:',user.latitude)
	print('user.longitude:',user.longitude)
	sql = '''select * from tbl_house AS p  ORDER BY POW(p.latitude - %s, 2) + POW(p.longitude - %s, 2) ASC;'''%(user.latitude, user.longitude)
	houselist = TblHouse.objects.raw(sql)

	# 确定house_id
	print('request.method:',request.method)
	house_id = request.GET.get('house_id',None)
	print('house_id from GET(switch):',house_id)
	if house_id:
		try:
			house = TblHouse.objects.filter(id=house_id)[0]
		except:
			return render_to_response('DiningServer/404.html')
		name = house.name
		location = house.location
		phone = house.phone
		open_time = house.open_time
		close_time = house.close_time
	else:
		try:
			house_id = houselist[0].id
			name = houselist[0].name
			location = houselist[0].location
			phone = houselist[0].phone
			open_time = houselist[0].open_time
			close_time = houselist[0].close_time
		except:
			house_id = request.session.get('house_id','')
			print('house_id in except:', house_id)
			try:
				house = TblHouse.objects.filter(id=house_id)[0]
			except:
				return render_to_response('DiningServer/404.html')
			name = house.name
			location = house.location
			phone = house.phone
			open_time = house.open_time
			close_time = house.close_time

	print('house_id finally:',house_id)
	
	category_and_meal.set_house(house_id=house_id,name=name,location=location,phone=phone,open_time=open_time,close_time=close_time)

	# for house in houselist:
	# 	category_and_meal.add_house(
	# 		house_id=house.id,
	# 		name=house.name,
	# 		location=house.location, 
	# 		phone=house.phone)
	# category_and_meal.set_house(id=1,name='三里屯店',location='三里屯soho地下美食广场', phone='1990009002')

	
	# 获取第一个分类的商品内容
	meal_list = TblMealInHouse.objects.filter(house_id=house_id,meal_status=MEAL_SHOW).order_by('category_id')
	for item in meal_list:
		if item.category_id in category_list:
			index = category_list.index(item.category_id)
		else:
			index = 0
		category_and_meal.add_meals(
			item.category_id,
			item.meal_id,
			item.name,
			item.avatar_url,
			item.detail_content,
			item.sold_count,
			item.judge_count,
			item.meal_price,
			item.last_count,
			index)
	if category_and_meal.to_dict()['meals'][-1] == []:
		del category_and_meal.to_dict()['meals'][-1]
	return category_and_meal.to_dict()

"""
获取商品详情
"""
def getMealDetailInHouse(meal_id,house_id):
	mealInHouse = interface.mealDetailInHouse()
	try:
		tbl_meal_in_house = TblMealInHouse.objects.filter(meal_id=meal_id)[0]
	except:
		return {}

	index = mealInHouse.getMealDetailInHouse(
										tbl_meal_in_house.id,
										tbl_meal_in_house.meal_id,
										tbl_meal_in_house.house_id,
										tbl_meal_in_house.category_id,
										tbl_meal_in_house.name,
										tbl_meal_in_house.avatar_url,
										tbl_meal_in_house.detail_url,
										tbl_meal_in_house.detail_content,
										tbl_meal_in_house.sold_count,
										tbl_meal_in_house.judge_count,
										tbl_meal_in_house.meal_price,
										tbl_meal_in_house.last_count,
										tbl_meal_in_house.add_time,
										tbl_meal_in_house.category_order,
										tbl_meal_in_house.meal_status,
										)
	try:
		house = TblHouse.objects.filter(id=house_id)[0]
	except:
		return {}
	mealInHouse.getHouse(
						house.id, 
						house.name, 
						house.latitude, 
						house.longitude, 
						house.location, 
						house.add_time, 
						house.phone,
						)

	return mealInHouse.toDict()


# def getMealDetailInHouse(meal_id):

# 	try:
# 		tbl_meal_in_house = TblMealInHouse.objects.filter(meal_id=meal_id)[0]
# 	except:
# 		return {}

# 	return interface.getMealDetailInHouse(
# 										tbl_meal_in_house.id,
# 										tbl_meal_in_house.meal_id,
# 										tbl_meal_in_house.house_id,
# 										tbl_meal_in_house.category_id,
# 										tbl_meal_in_house.name,
# 										tbl_meal_in_house.avatar_url,
# 										tbl_meal_in_house.detail_url,
# 										tbl_meal_in_house.detail_content,
# 										tbl_meal_in_house.sold_count,
# 										tbl_meal_in_house.judge_count,
# 										tbl_meal_in_house.meal_price,
# 										tbl_meal_in_house.last_count,
# 										tbl_meal_in_house.add_time,
# 										tbl_meal_in_house.category_order,
# 										tbl_meal_in_house.meal_status,
# 										)
	


"""
评价商品
"""
def judgeMeal(bill_id, meal_in_house_id, user_id, judge_meal, judge_speed, judge_service):

	judge_item = TblJudgeMeal()
	judge_item.id = uuid4()
	judge_item.add_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
	judge_item.bill_id = bill_id
	judge_item.meal_in_house = meal_in_house_id
	judge_item.user_id = user_id
	judge_item.judge_meal = judge_meal
	judge_item.judge_speed = judge_speed
	judge_item.judge_service = judge_service

	judge_item.save()

"""
获取评价详情
"""
def getMealJudge(bill_id):
	try:
		judge_item = TblJudgeMeal.objects.filter(bill_id=bill_id)[0]
	except:
		return render_to_response('DiningServer/404.html')
	return judge_item

"""
添加分类
"""
def addCategory(category_name):
	import logging
	logger = logging.getLogger('django')
	count = TblMealCategory.objects.count()
	item = TblMealCategory()
	item.name = category_name
	item.change_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
	item.id = uuid4()
	item.show_order = count + 1  # 显示顺序默认往后排
	item.save()
	return item

def addMealByScript(category_id, category_order, name):

	item = TblMealInHouse()
	item.id = uuid4()
	item.add_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
	item.avatar_url = 'http://p1.meituan.net/460.280/deal/__2722145__9710843.jpg'
	item.category_id = category_id
	item.category_order = category_order
	item.detail_content = '米饭：100克DDD菜：100克'
	item.detail_url = 'http://p1.meituan.net/460.280/deal/__2722145__9710843.jpg'
	item.house_id = '1'
	item.judge_count = 2
	item.last_count = 100
	# item.meal_id =
	item.meal_price = 10.0
	item.name = name
	item.sold_count = 120
	item.save()

"""
获取用户选定商品id的详情 并返回用户选择的数量
"""
def getMealsAndCount(post):

	meals_and_count = interface.MealsAndCount()
	for key in post:
		print('key:',key)
		tblMeal = TblMealInHouse.objects.filter(meal_id=key)
		for item in tblMeal:
			meals_and_count.add_meals(
				item.meal_id, 
				item.name,
				item.avatar_url,
				item.detail_content,
				item.sold_count,
				item.judge_count,
				item.meal_price,
				item.last_count,
				post[key]
			)
			break
	return meals_and_count.toDict()


def addMealToHouse():

	for house in TblHouse.objects.all():
		if house.id == 'houseiddefault':
			continue
		else:
			for meal in TblMealInHouse.objects.filter(house_id='houseiddefault'):
				TblMealInHouse.objects.create(
											id=uuid4(),
											meal_id=meal.meal_id,
											house_id=house.id,
											category_id=meal.category_id,
											name=meal.name,
											avatar_url=meal.avatar_url,
											detail_url=meal.detail_url,
											detail_content=meal.detail_content,
											sold_count=meal.sold_count,
											judge_count=meal.judge_count,
											meal_price=meal.meal_price,
											last_count=meal.last_count,
											add_time=meal.add_time,
											category_order=meal.category_order,
											meal_status=meal.meal_status
											)


def renameDirFile():
	import os
	files = os.listdir("/path/to/DiningHouse/media")
	for filename in files :
		print(filename)
		li = filename.split('.')
		if li[1] == "png":
			newname = li[0] + ".jpg"
			try:
				os.rename(filename, newname)
			except:
				print('file %s cannot rename!!!'%filename)

def renameDbFile():
	queryset = TblMealInHouse.objects.values_list('avatar_url','detail_url')

	for row in queryset:
		for field in row:
			print(field)
			if field.split('.')[-1] == 'png':
				newfield = field.replace('.png','.jpg')
				print(newfield)
				TblMealInHouse.objects.filter(avatar_url=field).update(avatar_url=field,detail_url=newfield)
			else: continue

from PIL import Image
import os
def changeImageSize():
	for filename in os.listdir('/path/to/DiningHouse/media'):
		print(filename)
		image_path = '/path/to/DiningHouse/media/' + filename
		print(image_path)
		try:
			img = Image.open(image_path)
			img = img.resize((600,600),Image.ANTIALIAS)
			# img.thumbnail((600,600),Image.ANTIALIAS)
			img.save(image_path,optimize=True,quality=50)
		except:
			print('file %s cannot converted!!!'%filename)

def changeFieldValue():
	# TblMealInHouse.objects.filter(meal_id='1eff6c43-9cc7-4ae8-a57b-fe4b284f2555').update(
	# 																					meal_price=float(3),
	# 																					name=u'美年达',
	# 																					)
	TblHouse.objects.create(id=uuid4(),name='家家总店',latitude=float(22.541419),longitude=float(114.048077),location='深圳福田区中电信息大厦',add_time=time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time())),phone=28483562)

	meal_list_in_house = list(set(TblMealInHouse.objects.values_list('meal_id',flat=True)))
	meal_list_total = list(TblMeal.objects.values_list('id',flat=True))
	for meal_id in meal_list_in_house:
		if meal_id not in meal_list_total:
			print(meal_id)
			meal = TblMealInHouse.objects.filter(meal_id=meal_id)[0]
			TblMeal.objects.create(
									id=meal.meal_id,
									house_id='houseiddefault',
									category_id=meal.category_id,
									name=meal.name,
									avatar_url=meal.avatar_url,
									meal_price=meal.meal_price,
									detail_content=meal.detail_content,
									add_time=meal.add_time,
									category_order=meal.category_order
									)