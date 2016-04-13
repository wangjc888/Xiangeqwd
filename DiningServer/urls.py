from django.conf.urls import url
from . import views


urlpatterns = [
    #for test
    url(r'^generatorMeals/$', views.generatorMeals),
    url(r'^[\s\S][^\/]/$', views.welcome, name='welcome'),

    # index  首页 url
    url(r'^index/$', views.index, name='index'),
    url(r'^switch/$', views.switch, name='switch'),

    # 评价商品
    url(r'^judgeMeal/', views.judgeMeal, name='judgeMeal'),
    # 获取商品评价
    url(r'^getMealJudge/$', views.getMealJudge, name='getMealJudge'),
    url(r'^getHouseJudge/$', views.getHouseJudge, name='getHouseJudge'),
    
    # 获取商品详情页面
    url(r'^getMealDetail/$', views.getMealDetail, name='getMealDetail'),

    # 获取我的资料 、更新资料
    url(r'^getMyDetailInfoPage/$', views.getMyDetailInfoPage, name='getMyDetailInfoPage'),
    url(r'^listMyDetailInfoPage/$', views.listMyDetailInfoPage, name='listMyDetailInfoPage'),
    url(r'^modifyMyDetailInfo/$', views.modifyMyDetailInfo, name='modifyMyDetailInfo'),
    url(r'^addMyDetailInfo/$', views.addMyDetailInfo, name='addMyDetailInfo'),
    # url(r'^deleteMyDetailInfo/$', views.deleteMyDetailInfo, name='deleteMyDetailInfo'),

    # 去下单页面
    url(r'^gotoOrderPage/$', views.gotoOrderPage, name='gotoOrderPage'),
    # 创建订单接口      返回创建订单成功并提示去支付  的界面
    url(r'^createOrder/$', views.createOrder, name='createOrder'),
    url(r'^notifyPay/$', views.notifyPay, name='notifyPay'),

    # 支付订单接口
    url(r'^getToken/$', views.getToken, name='getToken'),
    url(r'^createMenu/$', views.createMenu, name='createMenu'),

    #支付完成后转至订单页面
    url(r'^getOrder/$', views.getOrder, name='getOrder'),
    
    url(r'^ensureSend/$', views.ensureSend),
    
    # 获取我的订单页面 未付款 配送中 待评价
    url(r'^getOrdersByType/$', views.getOrdersByType, name='ordersByType'),
    url(r'^getBillDetail/$', views.getBillDetail, name='getBillDetail'),

]