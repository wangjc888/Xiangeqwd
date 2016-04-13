__author__ = 'liujiazhi'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.loginGuide, name='loginGuide'),
    url(r'^sign/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^pushPage/$', views.pushPage, name='pushPage'),
    #url(r'^loadDealRecord/$', views.loadDealRecord, name='loadDealRecord'),
    url(r'^schdule_task/$', views.schdule_task, name='schdule_task'),
    url(r'^deal_order/$', views.deal_order, name='deal_order'),
    url(r'^insert_order/$', views.insert_order, name='insert_order'),
    url(r'^print_order/$', views.print_order, name='print_order'),
    url(r'^show_order_detail/$', views.show_order_detail, name='show_order_detail'),
    url(r'^sure_arrive/$', views.sure_arrive, name='sure_arrive'),

]