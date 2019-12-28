import datetime
import hashlib
import random
import string

import xmltodict
from django.http.response import HttpResponse, JsonResponse
from apps.courses.models import Course
from apps.users.models import UserProfile
from apps.operations.models import UserFavorite,UserOpinion,UserOrder
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from utils.Code import deCryption
from hanmang.settings import order_url
import requests
import time

import json

wxinfo = {
    "APPID":'wxe6851ea0c162e8cf',
    "SECRET":'fd9f85627742e69506f8bc7bd07a2e6b',
    "MCHID":'1568039401',
    "MCHKEY":'HhCfnmreMdmb0KmaCQwlPDN9Im6BKlxp'
}

openidUrl = "https://api.weixin.qq.com/sns/jscode2session"
toOrderUrl = "https://api.mch.weixin.qq.com/pay/unifiedorder"

# Create your views here.

# 当用户点击时 查看添加收藏还是删除收藏
@csrf_exempt
def addFav(request):
    if request.method == "GET":
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        token = request.GET.get('token')  # 用户token
        key = request.GET.get("key")  # 课程id
        isCollection = request.GET.get("isCollection")  # 是否已经收藏
        openid = deCryption(token)
        '''
            如果isCollection 是true 说明已经收藏就取消收藏
            如果isCollection 是false 说明没有收藏就收藏
        '''
        if isCollection == 'true':
            # 通过openid 查找到用户
            user = UserProfile.objects.filter(openid=openid).first()
            # 通过user 查找用户的favlist
            favlist = UserFavorite.objects.filter(user_id=user.id)
            # 从收藏中删除 该课程
            favlist.filter(fav_id=key).delete()
            # 课程收藏数量-1
            course = Course.objects.get(id=key)
            course.fav_nums -= 1
            if course.fav_nums <= 0:
                course.fav_nums = 0
            course.save()
            print(course.fav_nums)
            # 返回isCollection 为false删除成功
            resp['msg'] = "操作成功"
            resp['data'] = {
                'isCollection': False
            }
            return HttpResponse(json.dumps(resp))
        else:
            # 通过openid 查询user 的id
            user = UserProfile.objects.filter(openid=openid).first()
            # 创建一个UserFavorite对象
            userFav = UserFavorite()
            userFav.user = user
            userFav.fav_id = key
            userFav.fav_type = 1
            userFav.save()
            # 课程收藏数量+1
            course = Course.objects.get(id=key)
            course.fav_nums += 1
            course.save()
            print(course.fav_nums)
            # 返回isCollection为true 添加成功
            resp['msg'] = "操作成功"
            resp['data'] = {
                'isCollection': True
            }
            return HttpResponse(json.dumps(resp))
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        return HttpResponse(json.dumps(resp))


# 判断列表课程是否已经收藏
@csrf_exempt
def isFav(request):
    if request.method == "GET":
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        key = int(request.GET.get("key"))
        token = request.GET.get("token")
        openid = deCryption(token)
        # 通过openid 查找到用户
        user = UserProfile.objects.filter(openid=openid)[0] # 没有收藏抛异常
        # 查询出用户的所有收藏
        favs = UserFavorite.objects.filter(user_id= user.id)
        flag = False    ## False表示没有收藏 True表示收藏了
        # 遍历用户所有收藏 查看有没有这个收藏
        for fav in favs:
            if fav.fav_id == key:
                flag = True
                break
        if flag:
            resp['data'] = {
                'flag':0 ## 0 表示收藏了
            }
            return HttpResponse(json.dumps(resp))
        else:
            resp['data'] = {
                'flag':-1 ## -1 表示没有收藏了
            }
            return HttpResponse(json.dumps(resp))


# 获取所有当前用户的收藏
@csrf_exempt
def getFav(request):
    if request.method == 'GET':
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        token = request.GET.get("token") # 获取token 解析出openid
        openid = deCryption(token)
        # 获取用户
        user = UserProfile.objects.filter(openid=openid)[0]
        # 获取用户收藏中所有收藏的课程的id
        favIdList = UserFavorite.objects.filter(user = user)

        courseList = []
        for fav in favIdList:
            course = Course.objects.filter(id = fav.fav_id)[0]
            courseList.append(course)
        courseList = serializers.serialize("json",courseList)

        return HttpResponse(courseList)
    else:
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        return HttpResponse(json.dumps(resp))


## 用户订单评价
@csrf_exempt
def setCollection(request):
    pass


## 用户意见
@csrf_exempt
def setOpinion(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":
        token = request.POST.get("token")
        openid = deCryption(token)

        content = request.POST.get("content")

        user = UserProfile.objects.filter(openid = openid)[0]
        opinion = UserOpinion(user=user,opinion=content).save()

        ## 操作成功
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': 500, 'msg': '操作失败', 'data': {}}
        return HttpResponse(json.dumps(resp))


## 获取用户页面数量
# 待测试
## 获取待评价的课程数量
@csrf_exempt
def getNum(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        token = request.GET.get("token")
        openid = deCryption(token)
        user = UserProfile.objects.filter(openid = openid)[0]

        noEvaluate = UserOrder.objects.filter(user=user).filter(is_Opinion = False).count() ## 未评价订单数量
        favNum = UserFavorite.objects.filter(user=user).count() ## 收藏数量
        orderNum = UserOrder.objects.all().count() #所有订单数量

        resp['data'] = {
            'noEvaluate': noEvaluate,
            'favNum':favNum,
            'orderNum':orderNum,
        }
        return HttpResponse(json.dumps(resp))
    else:
        resp['code'] = 500;
        resp['msg'] = '操作失败'
        return HttpResponse(json.dumps(resp))



'''
    统一下单支付接口
'''
@csrf_exempt
def payOrder(request):
    if request.method == 'POST':
        # 获取价格
        price = float(request.POST.get("price"))
        # 获取课程id
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)
        # 获取客户端ip
        # client_ip, port = request.get_host().split(":")
        # 获取小程序openid
        token = request.POST.get("token")
        openid = deCryption(token) # 创建订单的用户
        user = UserProfile.objects.get(openid=openid) #拿到用户 做订单创建存储
        nonce_str = randomStr()
        now_time = datetime.datetime.now() # 订单创建时间
        out_trade_no = str(now_time.year)+str(random.randrange(1000000,99999999)) # 商户订单号
        body = course.name +":"+ course.desc
        params = {
            'appid':wxinfo['APPID'],
            'mch_id':wxinfo['MCHID'],
            'openid':openid,
            'nonce_str':nonce_str,
            'body':body, # 获取到的商品的内容 商品的名字
            'out_trade_no': out_trade_no,
            'total_fee':'10', #　商品课程的价格
            'spbill_create_ip':'192.168.80.39', # 本地ip地址
            'notify_url':'https://baidu.com/pay-res', # 还没有写的回调函数地址
            'trade_type':'JSAPI',
        }
        sign = wx_sign(params)
        params['sign'] = sign
        print(params)
        xmlmsg = send_xml_request(toOrderUrl,params)
        data = {}

        if xmlmsg['xml']['return_code'] == 'SUCCESS':
            prepay_id = xmlmsg['xml']['prepay_id']
            timeStamp = str(int(time.time()))
            data = {
                'appId': wxinfo['APPID'],
                'nonceStr': nonce_str,
                'package': "prepay_id=" + prepay_id,
                'signType': 'MD5',
                'timeStamp': timeStamp
            }
            paySign = wx_sign(data)
            data['paySign'] = paySign
            print(data)
        ## 创建订单 将支付状态设置为 待付款 存储
        userOrder = UserOrder(
            user=user,
            course=course,
            order_sn=out_trade_no,
            pay_price=course.price,
            pay_time=None, #在回调函数中 若支付成功 设置支付时间
            created_time=now_time,
            order_desc=body,
            order_Opinion=None,
            is_Opinion=False,
            is_Pay=False #在回调函数中 若支付成功 把他设置为True
        ).save()
        # 为学习人数加一
        course.students += 1

        return HttpResponse(json.dumps(data))
    else:
        resp = {'code': 500, 'msg': '请求类型错误,请求失败', 'data': {}}
        return HttpResponse(json.dumps(resp))

# 将字典转换为xml 发送到微信服务器
def send_xml_request(url,param):
    param = {'xml':param}
    xml = xmltodict.unparse(param)
    print(xml)
    response = requests.post(url,data=xml.encode('UTF8'),headers={
        'Content-Type':'charset=utf-8'
    })
    msg = response.text
    print(response.content.decode('utf-8'))

    xmlmsg = xmltodict.parse(msg)
    return xmlmsg



# 生成随机字符串
def randomStr():
    return ''.join(random.sample(string.ascii_letters+string.digits,32))


# 算法签名
def wx_sign(param):
    stringA = ""
    ks = sorted(param.keys())
    for k in ks:
        stringA += (k + '=' + param[k] + '&')

    stringSignTemp = stringA + "key=" + wxinfo['MCHKEY']

    hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()
    return sign

'''
    统一下单支付接口
'''

# 获取所有的用户订单
def userOrders(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        token = request.GET.get("token")
        openid = deCryption(token)
        user = UserProfile.objects.filter(openid = openid)[0]
        orders = UserOrder.objects.values().filter(user=user)
        orders_list = list(orders)
        print(type(orders_list))
        return HttpResponse(orders_list)
    else:
        resp['code'] = 500
        resp['msg'] = "请求类型错误操作失败"
        return HttpResponse(json.dumps(resp))