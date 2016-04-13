__author__ = '祥祥'

from django.conf.urls import url
from . import views
from DiningHouse import settings
"""
count : 统计 一般表示统计图的数据
"""

urlpatterns = [
    url(r'^login/$', views.loginGuide, name='loginGuide'),
    url(r'^sign/$', views.login, name='login'),

    url(r'^regist/$',views.regist,name = 'regist'),
    # url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    # 首页
    url(r'^index/$', views.index, name='index'),
    #house_id is pure num
    ##url(r'^(?P<house_id>[0-9]*)/index/$', views.index, name='index'),
    # 用户部分url
    url(r'^getUserAllCountInfo/$', views.getUserAllCountInfo, name='getUserAllCountInfo'),#获取所有每日注册用户的统计

    #用户统计部分全部放到getUserAllCountInfo中处理
    #url(r'^getUserNumber/$', views.getUserNumber, name='getUserNumber'),
    # url(r'^getUserCount/$', views.getUserCount, name='getUserCount'),
    # 订单部分url
    url(r'^getOrderCount/$', views.getOrderCount, name='getOrderCount'),
    url(r'^getOrderList/$', views.getOrderList, name='getOrderList'),
    url(r'^delOrder/$', views.delOrder, name='delOrder'),#删除订单列表
    # 餐品部分url
    url(r'^getMealList/$', views.getMealList, name='getMealList'),
    # url(r'^(?P<house_id>[0-9]*)/getMealList/$', views.getMealList, name='getMealList'),
    #url(r'^updateMealInfo/$', views.updateMealInfo, name='updateMealInfo'),
    url(r'^getUpdateMeal/$', views.getUpdateMeal, name='getUpdateMeal'),
    url(r'^addMeal/$', views.addMeal, name='addMeal'),
    url(r'^copyMeal/$', views.copyMeal, name='copyMeal'),
    url(r'^delMeal/$', views.delMeal, name='delMeal'),#删除菜品信息（下架）
    url(r'^getMealAndPrice/$', views.getMealAndPrice, name='getMealAndPrice'),#删除菜品信息（下架）
    url(r'^modifyPrice/$', views.modifyPrice, name='modifyPrice'),
    url(r'^comparePrice/$', views.comparePrice, name='comparePrice'),
    url(r'^getCreateMeal/$', views.getCreateMeal, name='getCreateMeal'),
    url(r'^updateMeal/$', views.updateMeal, name='updateMeal'),
    # 分店部分url
    url(r'^getHouses/$', views.getHouses, name='getHouses'),
    # url(r'^(?P<house_id>[0-9]*)/getHouses/$', views.getHouses, name='getHouses'),
    url(r'^addHouse/$', views.addHouse, name='addHouse'),
    url(r'^updateHouseInfo/$', views.updateHouseInfo, name='updateHouseInfo'),
    url(r'^getUpdateHouse/$', views.getUpdateHouse, name='getUpdateHouse'),
    url(r'^delHouse/$', views.delHouse, name='delHouse'),#删除分店信息
    # 评价部分的url
    url(r'^getAllJudge/$', views.getAllJudge, name='getAllJudge'),
    # url(r'^(?P<house_id>[0-9]*)/getAllJudge/$', views.getAllJudge, name='getAllJudge'),
    url(r'^getJudgeDistribute/$', views.getJudgeDistribute, name='getJudgeDistribute'),
    url(r'^loadJudge/$', views.loadJudge, name='loadJudge'),
    url(r'^delJudge/$', views.delJudge, name='delJudge'),#删除评价信息
    # url(r'^(?P<house_id>[0-9]*)/getJudgeDistribute/$', views.getJudgeDistribute, name='getJudgeDistribute'),

    #获取统计报表
    url(r'^getStatement/$', views.getStatement, name='getStatement'),
    # url(r'^test/$', views.test, name='test'),
    url(r'^uploadPic/$', views.uploadPic, name='uploadPic'),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT})

]