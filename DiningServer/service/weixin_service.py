# -*- encoding=utf-8 -*- 
# import httplib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from DiningHouse.settings import *
from DiningServer.models import *

from DiningServer.common.weixin_pay.weixin_pay import UnifiedOrderPay
from DiningServer.common.weixin_pay.weixin_pay import JsAPIOrderPay
from DiningServer.common.weixin_pay.weixin_pay import OrderQuery
from DiningServer.common.weixin_pay.weixin_pay import Refund
from DiningServer.common.weixin_pay.weixin_pay import RefundQuery
from DiningServer.common.weixin_pay.weixin_pay import WechatPush

import http.client, urllib,requests,time


#调用统一下单API
def callOrderAPI(request,body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid):
    
    pay = UnifiedOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)

    response = pay.post(body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid)

    for k,v in response.items():
        print('response:',k.encode('utf-8'),v.encode('utf-8'))
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        request.session['prepay_id'] = response["prepay_id"]
        return response
    else:
        if response["return_code"] == "FAIL":
            err_code_des = response["return_msg"]
            return None
            #通信失败处理
        try:
            response["result_code"] == "FAIL"
            err_code = response["err_code"]
            err_code_des = pay.get_error_code_desc(response["err_code"])
            #交易失败处理
        except:
            pass


#生成JSAPI页面调用的支付参数并签名
def genJsAPIParams(prepay_id):
    pay = JsAPIOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY,WC_PAY_APPSECRET)

    js_params = pay._get_json_js_api_params(prepay_id)

    return js_params

#查询支付结果
def callQueryPayResult(out_trade_no):
    pay = OrderQuery(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)
    response = pay.post(out_trade_no)
    for k,v in response.items():
        print('payResult:', k,v)
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        if response["trade_state"] == "SUCCESS": #支付成功
            return True
        else:
            return False
    else: return False

#根据code获取openid
def getOpenid(request,redirect_uri):
    pay = JsAPIOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY,WC_PAY_APPSECRET)

    code = getCode(request,redirect_uri)
    print('code for openid:',code)
    openid = pay._get_openid(code)
    return openid

def getCode(request,redirect_uri):
    pay = JsAPIOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY,WC_PAY_APPSECRET)

    #先判断request.GET中是否有code参数，如果没有，需要使用create_oauth_url_for_code函数获取OAuth2授权地址后重定向到该地址并取得code值
    
    if 'code' not in request.GET:
        oauth_url = pay.create_oauth_url_for_code(redirect_uri)
        # print('oauth_ur:',oauth_url)
        return HttpResponseRedirect(oauth_url)
        # return requests.get(oauth_url)
    else:
        return request.GET.get('code', None)  


# 申请退款
def refund(request,out_trade_no, out_refund_no, total_fee, refund_fee, op_user_id):
    refund = Refund(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)
    response = refund.post(out_trade_no, out_refund_no, total_fee, refund_fee, op_user_id)
    for k,v in response.items():
        print('refund_response:',k,v)
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        return True
    else:
        return False 

# 退款查询
'''提交退款申请后，通过调用该接口查询退款状态。退款有一定延时，用零钱支付的退款20分钟内到账，银行卡支付的退款3个工作日后重新查询退款状态。'''

def refundQuery(request, out_trade_no):
    refundQuery = RefundQuery(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)
    response = refundQuery.post(out_trade_no)
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS" and response["refund_status_$n"] == "SUCCESS":
        return True
    else:
        return False

# 发送模板消息
def sendTplMsg(request, touser, template_id, url, data):
    wechatPush = WechatPush(WC_PAY_APPID, WC_PAY_APPSECRET)
    response = wechatPush.pushMsg(touser, template_id, url, data)
    for k,v in response.items():
        print('sendTplMsg response:',k,v)
    if response and response["errmsg"] == "ok":
        return True
    else:
        return False


    # {
    #    "touser":"OPENID",
    #    "template_id":"6E5y5UZsExW45VywamzEzk7eyf8eOM1KXKSzJyU5NHQ", 
    #    "url":"http://weixin.qq.com/download",            
    #    "data":{
    #            "first": {
    #                "value":"商家拒绝接单通知",
    #                "color":"#173177"
    #            },
    #            "订单编号":{
    #                "value":"您选购的菜品已经售完，商家拒绝接单",
    #                "color":"#C4C400"
    #            },
    #            "下单时间": {
    #                "value":"退款有一定延时，用零钱支付的退款20分钟内到账，银行卡支付的退款3个工作日后重新查询退款状态",
    #                "color":"#173177"
    #            },
    #            "拒绝时间": {
    #                "value":"2014年9月22日",
    #                "color":"#173177"
    #            },
    #            "拒绝理由": {
    #                "value":"2014年9月22日",
    #                "color":"#FF0000"
    #            },
    #            "remark":{
    #                "value":"欢迎另选其它菜品！",
    #                "color":"#008000"
    #            }
    #    }
    # }