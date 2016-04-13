__author__ = 'liujiazhi'
#负责导出用户评价数据到excel(这里可以设置导出不同的数据，不仅仅限于用户评价信息，也可以导出餐品信息)
from DiningOAM.models import TblAdminuser
from DiningOAM.models import TblJudgeMeal
from DiningOAM.models import TblBill
from DiningOAM.models import TblBillMeal

from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist
import xlwt
# import collections

def loadJudgeAsExcel(name, post):
    user = TblAdminuser.objects.get(username = name)
    house_id = user.getHouseId()
    min_time = post.get('min', 1)
    max_time = post.get('max', 1)
    # house_id = 1#for test
    if min_time == 1 and max_time == 1:#如果没有输入时间范围
        # 默认输出当前house_id的所有评价信息
        # print('output all judge info')
        judgeInfoSet = TblJudgeMeal.objects.filter(house_id=house_id).values('id', 'house_id', 'bill_id', 'meal_in_house', 'openid', 'user_name', 'judge_meal', 'judge_speed', 'judge_service', 'add_time')
        recordNum = TblJudgeMeal.objects.filter(house_id=house_id).count()
    else:
        min_time_tuple = tuple(time.strptime(min_time, '%Y-%m-%d'))
        max_time_tuple = tuple(time.strptime(max_time, '%Y-%m-%d'))#将str转换成元组再转换成datetime类型
        start_time = datetime.datetime(min_time_tuple[0], min_time_tuple[1], min_time_tuple[2])
        end_time = datetime.datetime(max_time_tuple[0], max_time_tuple[1], max_time_tuple[2])
        judgeInfoSet = TblJudgeMeal.objects.filter(house_id=house_id, add_time__in = [start_time, end_time]).values()
        recordNum = TblJudgeMeal.objects.filter(house_id=house_id, add_time__in = [start_time, end_time]).count()
    print('judgeInfoSet:', judgeInfoSet, 'type:', type(judgeInfoSet))#查询集字典中的数据信息并不是按照字段顺序显示
    f = xlwt.Workbook()#创建工作簿
    #创建第一个sheet
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok = True)
    row0 = [u'评价ID', u'分店ID', u'订单ID', u'菜品名', u'用户ID', u'菜品评价', u'送餐速度评价', u'服务质量评价',u'评价详情', u'评价时间']
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))#True设置字体加粗

    for i in range(0, recordNum):
        sheet1.write(i+1, 0, judgeInfoSet[i]['id'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 1, judgeInfoSet[i]['house_id'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 2, judgeInfoSet[i]['bill_id'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 3, judgeInfoSet[i]['meal_in_house'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 4, judgeInfoSet[i]['openid'], set_style('Time New Roman', 200))
        # sheet1.write(i+1, 5, judgeInfoSet[i]['username'], set_style('Time New Roman', 200, True))
        sheet1.write(i+1, 5, judgeInfoSet[i]['judge_meal'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 6, judgeInfoSet[i]['judge_speed'], set_style('Time New Roman', 200))
        sheet1.write(i+1, 7, judgeInfoSet[i]['judge_service'], set_style('Time New Roman', 200))
        # sheet1.write(i+1, 8, judgeInfoSet[i]['judge_service'], set_style('Time New Roman', 200))#用户评价详情，这个需要在表单中增加字段
        sheet1.write(i+1, 9, judgeInfoSet[i]['add_time'].strftime('%Y-%m-%d %H:%I:%S'), set_style('Time New Roman', 200))
    # for j in range(0, len(testList)):
    #     for i in range(0, len(row0)):
    #         sheet1.write(j+1, i, testList[j], set_style('Time New Roman', 200, True))
    f.save('评价详情.xlsx')        #在当前project目录下生成Excel
    # f.save('C:/test1.xlsx')#在C盘根目录下生成excel文件
    return '成功导出数据到当前目录下'

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()

    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


#生成报表
def createStatement():
    houseandbillDict = {}
    mealsoldcountDict = {}
    sheetDict = {'house_name':[],'total_amount':[], 'total_sold_cnt':[]}#当前销售总金额，销售订单总量
    houseNameId={}
    houseSet = TblAdminuser.objects.all()
    for item in houseSet:
        houseNameId.update({item.house_id:item.house_name})
    print('houseNameId:',houseNameId)
    id_list = TblAdminuser.objects.values_list('house_id', flat=True)#获取当前所有登录用户的house_id,以列表返回
    print('id_list:',id_list)
    for key in id_list:
        total_billDict = TblBill.objects.filter(house_id=key).aggregate(Sum('bill_totalling'))#每分店销售总额
        sold_cntDict = TblBillMeal.objects.filter(house_id=key).aggregate(Sum('buy_count'))#每分店销售菜品总数
        total_bill = (total_billDict['bill_totalling__sum'] if total_billDict['bill_totalling__sum'] is not None else 0.0)
        total_sold_cnt = (sold_cntDict['buy_count__sum'] if sold_cntDict['buy_count__sum'] is not None else 0)
        houseandbillDict.update({key:total_bill, })
        mealsoldcountDict.update({key:total_sold_cnt, })
        print('total_bill:',total_bill, 'sold_cnt:',total_sold_cnt)
    print('housebilldict:',houseandbillDict)
    bill_sort = sorted(houseandbillDict.items(), key=lambda houseandbillDict:houseandbillDict[1], reverse=1)#按value排序，即按总金额排序（从大到小）
    print('bill_sort:',bill_sort)
    for key1 in bill_sort:
        print('key1:', key1)
        sheetDict['total_amount'].append(key1[1])
        sheetDict['total_sold_cnt'].append(mealsoldcountDict[key1[0]])#以id，查找对应的销售数量
        sheetDict['house_name'].append(houseNameId[key1[0]])#以id查找当前的店面名称
    print('sheet:',sheetDict)
    return sheetDict




# def createStatement(post):
#     #houseSheet = [] #[{'house_name':name1,'total_bill':bill, 'meal': [], 'sold_cnt':[]},{'house_name':name2}]#各分店报表统计
#     houseandbillDict = {}
#     mealsoldcountDict = {}
#     sheetDict = {'house_name':[],'total_amount':[], 'total_sold_cnt':[]}#当前销售总金额，销售订单总量
#     id_list = TblAdminuser.objects.values_list('house_id', flat=True)#获取当前所有登录用户的house_id,以列表返回
#     print('id_list:',id_list)
#     #i = 0
#     for key in id_list:
#         total_billDict = TblBill.objects.filter(house_id=key).aggregate(Sum('bill_totalling'))#每分店销售总额
#         sold_cntDict = TblBill.objects.filter(house_id=key).aggregate(Sum('buy_count'))#每分店销售菜品总数
#         total_bill = total_billDict['bill_totalling__sum']
#         total_sold_cnt = sold_cntDict['buy_count__sum']
#         houseandbillDict.update({key:total_bill, })
#         mealsoldcountDict.update({key:total_sold_cnt, })
#
#         #houseSheet[i]['total_bill']=total_bill['bill_totalling__sum']
#         print('total_bill:',total_bill, 'sum:',total_bill['bill_totalling__sum'], 'sold_cnt:',total_sold_cnt)
#         #meal_list = TblBillMeal.objects.filter(house_id=key).values_list('meal_name', flat=True)#求本店面所有已经被售菜品
#         #for key2 in meal_list:
#         #    meal_sold_cnt = TblBillMeal.objects.filter(house_id=key, meal_name=key2).aggregate(Sum('buy_count'))#同一店面同一菜品的销量
#             #houseSheet[i]['meal'].append(key2)#菜品名
#             #houseSheet[i]['sold_cnt'].append(meal_sold_cnt)#销售数量
#             #mealandcountDict.update({key2:meal_sold_cnt})#key(菜品名)：value(销售数量)
#         #i += 1
#
#     bill_sort = sorted(houseandbillDict.items(), key=lambda houseandbillDict:houseandbillDict[1])#按value排序，即按总金额排序（从小到大）
#
#     # sold_cnt_sort = sorted(mealandcountDict.items(), key=lambda mealandcountDict:mealandcountDict[1])#按销售数量给菜品排序(暂未以菜品销售数量排序)
#     sheetDict['total_amount'].append(test1['bill_totalling__sum'])#销售总额
#         # sheetDict['total_sold_cnt'].append(bill_cnt)#订单总数
#
#         # print('key:',key, 'bill_list:', bill_list, 'total:', total)
#     return sheetDict