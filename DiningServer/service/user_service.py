from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from DiningServer.models import TblUser

from DiningServer.common.time_format_util import SERVER_DATA_FORMAT
import time

SEX = {
    # 从数据库得到数值 从下面得到对应的性别
    1 : '男',
    2 : '女',

    # web端传过来 男女，从下面获取对应的数值
    '男' : 1,
    '女' : 2,
}

(NO_DEFAULT,SET_DEFAULT)=range(2)
user_default = [
            (NO_DEFAULT, '非默认地址'),
            (SET_DEFAULT,'默认地址'),
            ]

(ALLOW,DENY)=range(2)
user_access = [
            (ALLOW, '允许'),
            (DENY,'禁止'),
            ]

# 获取用户详细信息
def getMyDetailInfo(openid):
    if not openid:
        return {}
    
    try:
        user = TblUser.objects.filter(openid=openid, default=SET_DEFAULT).order_by('-add_time')[0]
    except:
        user = TblUser.objects.filter(openid=openid,access=ALLOW).order_by('-add_time')[0]
    detail_info =  {
        'id' : user.id,
        'openid' : user.openid,
        'username' : user.username,
        'sex' : user.sex,
        'phone' : user.phone,
        'user_location' : user.user_location
    }
    return detail_info


# 更改用户详细信息
# def modifyMyDetailInfo(openid,username, sex, phone, add_time, location, latitude, longitude):

#     TblUser.objects.filter(openid=openid).update(
#                                             username=username,
#                                             sex=sex,
#                                             phone=phone,
#                                             add_time=add_time,
#                                             user_location=location,
#                                             latitude=float(latitude),
#                                             longitude=float(longitude)
#                                             )