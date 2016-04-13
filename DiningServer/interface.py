__author__ = '祥祥'

"""
页面中获取到的数据
"""



# 首页显示的菜品及内容接口
class CategoryAndMeal():
    """
    最后的context的效果示例
    context = {
        # _banners
        'banners':[
            {
                image_url: '这里是图片路径',
                link: '点击后跳转的url'
            },
            {
                image_url: '这里是图片路径',
                link: '点击后跳转的url'
            }
        ]
        # 分店内容  字典表示
        houselist : [
            {
                'house_id': '分店id'
                'name': '分店名字1',
                'location': '分店位置'
                'phone': '分店电话'
            }
            {
                'house_id': '分店id'
                'name': '分店名字2',
                'location': '分店位置'
                'phone': '分店电话'
            }
        ]
        # 分类及菜品 数组
        categorys: [
            # 每一项的分类 字典表示
            {
                'category': '分类1',    # 分类名称
                'category_id': 1,       # 分类id
            },
            {
                'category': '分类2',    # 分类名称
                'category_id': 2,       # 分类id
            },
            {
                'category': '分类3',    # 分类名称
                'category_id': 3,       # 分类id
            },

        ]
        #分类中的菜品 数组表示
        'meals':[
                    [
                        #菜品中的对象 字典表示
                        {   'category_id': 1,
                            'meals_id': 1,      # meal id
                            'meals_name': '我是菜名',    # 名称
                            'avatar_url': '我是图片地址',    # avatar_ur 显示的小图
                            'content': '我是描述使用 ddd 分隔每一行的内容',
                            'sold_count': 10,            #售出量
                            'judge_count': 10,           #评价量
                            'meal_price':  10.0,         #单价 元
                            'last_count': 20,            #剩余量  0 表示卖完了
                        },
                        {   
                        },
                    ]
                    [   {   'category_id': 1,
                            'meals_id': 1,      # meal id
                            'meals_name': '我是菜名',    # 名称
                            'avatar_url': '我是图片地址',    # avatar_ur 显示的小图
                            'content': '我是描述使用 ddd 分隔每一行的内容',
                            'sold_count': 10,            #售出量
                            'judge_count': 10,           #评价量
                            'meal_price':  10.0,         #单价 元
                            'last_count': 20,            #剩余量  0 表示卖完了
                        },
                        {
                        },
                    ]
                ]
    }

    """


    def __init__(self):
        self._context = {}
        self._house = {}
        # self._houselist = []
        self._category_and_meal = []
        self._banners = []
        self._meals = [[]]
        self._context['house'] = self._house
        # self._context['houselist'] = self._houselist
        self._context['banners'] = self._banners
        self._context['categorys'] = self._category_and_meal
        self._context['meals'] = self._meals

    def set_house(self, house_id, name, location, phone,open_time,close_time):
        self._house['house_id'] = house_id
        self._house['name'] = name
        self._house['location'] = location
        self._house['phone'] = phone
        self._house['open_time'] = open_time
        self._house['close_time'] = close_time

    # def add_house(self, house_id, name, location, phone):
    #     self._houselist.append({
    #         'house_id': house_id,
    #         'name': name,
    #         'location': location,
    #         'phone': phone
    #     })

    def add_banner(self, image_url='', link=''):
        self._banners.append({
            'image_url':image_url,
            'link': link
        })

    def add_category_and_meals(self, category='', category_id=''):
        self._category_and_meal.append({
            'category': category,
            'category_id': category_id
        })
        self._meals.extend([[]])

    def add_meals(self, category_id, meal_id, meal_name, avatar_url, content, sold_count, judge_count, meal_price, last_count, index):
        self._meals[index].append({
            'category_id': category_id,
            'meal_id': meal_id,
            'meal_name': meal_name,
            'avatar_url': avatar_url,
            'content': content,
            'sold_count': sold_count,
            'judge_count': judge_count,
            'meal_price': meal_price,
            'last_count': last_count,
        })


    def to_dict(self):
        print('餐品的数量', len(self._meals))
        return self._context

# 根据内容构造 商品详情的字典
class mealDetailInHouse():

    def __init__(self):
        self._context = {}

    def getMealDetailInHouse(self, id, meal_id, house_id, category_id, name, avatar_url, detail_url, detail_content, sold_count, judge_count, meal_price, last_count, add_time, category_order, meal_status):
        meal = {
                'id': id,
                'meal_id':meal_id,
                'house_id':house_id,
                'category_id':category_id,
                'name': name,
                'avatar_url': avatar_url,
                'detail_url': detail_url,
                'detail_content': detail_content,
                'sold_count': sold_count,
                'judge_count': judge_count,
                'meal_price': meal_price,
                'last_count': last_count,
                'add_time': add_time,
                'category_order': category_order,
                'meal_status': meal_status,
                }
        self._context['meal'] = meal

    def getHouse(self, id, name, latitude, longitude, location, add_time, phone):
        house = {
            'id' : id,
            'name' : name,
            'latitude' : latitude,
            'longitude' : longitude,
            'location' : location,
            'add_time' : add_time,
            'phone' : phone,
        }
        self._context['house'] = house

    def toDict(self):
        return self._context

# 根据内容构造 商品详情的字典
class billDetail():

    def __init__(self):
        self._context = {}
        self._meals = []
    def getBillDetail(self, id, prepay_id, house_id, openid, user_id, user_location, door, bill_totalling, delivery_fee, all_fee, add_time, pay_time, bill_state, bill_content, ensure_send_time):
        bill = {
                'id': id,
                'prepay_id':prepay_id,
                'house_id':house_id,
                'openid':openid,
                'user_id': user_id,
                'user_location': user_location,
                'door': door,
                'bill_totalling': bill_totalling,
                'delivery_fee': delivery_fee,
                'all_fee': all_fee,
                'add_time': add_time,
                'pay_time': pay_time,
                'bill_state': bill_state,
                'bill_content': bill_content,
                'ensure_send_time': ensure_send_time,
                }
        self._context['bill'] = bill

    def addMeal(self, id, meal_id, house_id, bill_id, openid, user_id, buy_count, add_time, meal_name, meal_url, meal_price):
        meal = {
                'id': id,
                'meal_id':meal_id,
                'house_id':house_id,
                'bill_id':bill_id,
                'openid': openid,
                'user_id': user_id,
                'buy_count': buy_count,
                'add_time': add_time,
                'meal_name': meal_name,
                'meal_url': meal_url,
                'meal_price': meal_price,
                'meal_price': meal_price,
                }
        self._meals.append(meal)
        self._context['meals'] = self._meals

    def getHouse(self, id, name, latitude, longitude, location, add_time, phone):
        house = {
            'id' : id,
            'name' : name,
            'latitude' : latitude,
            'longitude' : longitude,
            'location' : location,
            'add_time' : add_time,
            'phone' : phone,
        }
        self._context['house'] = house

    def toDict(self):
        return self._context

# 用于构造我的订单页面的返回值
class MyBills():

    def __init__(self):
        self._context = {}
        # bills 是一个账单列表  每个账单包含账单的信息,一个餐品列表,分店信息
        self._bills = []
        self._context['bills'] = self._bills

    def createMyBill(self, id, prepay_id, house_id, openid, user_id, user_location, door, bill_totalling, delivery_fee, all_fee, add_time, pay_time, bill_state, bill_content, ensure_send_time):
        bill = {
            'id': id,
            'prepay_id': prepay_id,
            'house_id' : house_id,
            'openid'   : openid,
            'user_id'   : user_id,
            'user_location' : user_location,
            'door' : door,
            'bill_totalling': bill_totalling,
            'delivery_fee': delivery_fee,
            'all_fee': all_fee,
            'add_time': add_time,
            'pay_time': pay_time,
            'bill_state' : bill_state,
            'bill_content': bill_content,
            'ensure_send_time': ensure_send_time,
            'meals': [],
            'house': {},
        }
        self._bills.append(bill)
        return len(self._bills) - 1

    def addMeal(self, id, meal_id, house_id, bill_id, openid, user_id, buy_count, add_time, meal_name, meal_url, meal_price, index):
        meal = {
            'id' : id,
            'meal_id' : meal_id,
            'house_id' : house_id,
            'bill_id' : bill_id,
            'openid' : openid,
            'user_id' : user_id,
            'buy_count' : buy_count,
            'add_time' : add_time,
            'meal_name' : meal_name,
            'meal_url' : meal_url,
            'meal_price' : meal_price,
        }
        try:
            self._bills[index]['meals'].append(meal)
        except:
            return None
        return 'success'

    def addHouse(self, id, name, latitude, longitude, location, add_time, phone, index):
        house = {
            'id' : id,
            'name' : name,
            'latitude' : latitude,
            'longitude' : longitude,
            'location' : location,
            'add_time' : add_time,
            'phone' : phone,
        }
        try:
            self._bills[index]['house'].update(house)
        except:
            return None
        return 'success'

    def toDict(self):
        return self._context

"""
餐品和它对应的数量
"""
class MealsAndCount():
    def __init__(self):
        self._context = {}
        self._meal_list = []
        self._context['meal_list'] = self._meal_list

    def add_meals(self, meal_id, meal_name, avatar_url, content, sold_count, judge_count, meal_price, last_count, buy_count):
        self._meal_list.append({
            'meal_id': meal_id,
            'meal_name': meal_name,
            'avatar_url': avatar_url,
            'content': content,
            'sold_count': sold_count,
            'judge_count': judge_count,
            'meal_price': meal_price,
            'last_count': last_count,
            'buy_count' : buy_count,
        })

    def toDict(self):
        return self._context


"""
店面评价
"""
class getHouseJudgeSet():

    def __init__(self):
        self._context = {}
        self._judgeList = []
        self._context['judgeList'] = self._judgeList

        self._context['good'] = 0
        self._context['soso'] = 0
        self._context['bad'] = 0

    def addJudgeToHouse(self, id, house_id, bill_id, meal_id, user_id, judge_meal, judge_speed, judge_message, add_time):
        judge = {
                'id': id,
                'house_id':house_id,
                'bill_id':bill_id,
                'meal_id':meal_id,
                'user_id': user_id,
                'judge_meal': judge_meal,
                'judge_speed': judge_speed,
                'judge_message': judge_message,
                'add_time': add_time,
                }
        self._judgeList.append(judge)
        return len(self._judgeList) - 1

    def setUserPhone(self, phone, index):
        if not phone:
            self._judgeList[index]['user_phone'].replace('','***********')
        else:
            phone_show = str(phone)[:3] + '****' + str(phone)[-4:]
            print('phone_show:',phone_show)
            self._judgeList[index]['user_phone'] = phone_show

    def setJudgeType(self, judge_meal, judge_speed, index):
        if int(judge_meal) + int(judge_speed) >= 7:
            self._judgeList[index]['judge_type'] = 1
        elif int(judge_meal) + int(judge_speed) >= 5:
            self._judgeList[index]['judge_type'] = 2
        else:
            self._judgeList[index]['judge_type'] = 3

    def getHouse(self, id, name, latitude, longitude, location, add_time, phone):
        house = {
            'id' : id,
            'name' : name,
            'latitude' : latitude,
            'longitude' : longitude,
            'location' : location,
            'add_time' : add_time,
            'phone' : phone,
        }
        self._context['house'] = house

    def calJudge(self, judge_meal, judge_speed):
        if int(judge_meal) + int(judge_speed) >= 7:
            self._context['good'] += 1
        elif int(judge_meal) + int(judge_speed) >= 5:
            self._context['soso'] += 1
        else:
            self._context['bad'] += 1
    
    def toDict(self):
        return self._context