from django.shortcuts import render
from django.shortcuts import render
from django.http.response import HttpResponse
from apps.courses.models import Course
from apps.users.models import UserProfile
from apps.operations.models import UserFavorite,UserOpinion,UserOrder
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from utils.Code import deCryption
from utils.WeChatPay import get_bodyData,get_paysign,xml_to_dict
from hanmang.settings import order_url
import requests
import time

import json

# Create your views here.

# 当用户点击时 查看添加收藏还是删除收藏
@csrf_exempt
def addFav(request):
    ## 获取所有收藏
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
            # 存储对象 收藏成功
            userFav.save()

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

# 待测试
## 获取所有订单
@csrf_exempt
def getOrder(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":
        token = request.POST.get("token")
        openid = deCryption(token)
        user = UserProfile.objects.filter(openid = openid)[0]
        userOrders = UserOrder.objects.filter(user=user)
        serializers.serialize("json",userOrders)
        resp['data'] = userOrders
        return HttpResponse(json.dumps(resp))
    else:
        resp['code'] = 500
        resp['msg'] = "操作失败"
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
        user = UserProfile.objects.filter(openid=openid)[0]
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

        openid = request.POST.get("token").split("#")[1] # 获取token 解析出openid
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



# 统一下单支付接口
@csrf_exempt
def payOrder(request):
    if request.method == 'POST':
        # 获取价格
        price = request.POST.get("price")

        # 获取客户端ip
        client_ip, port = request.get_host().split(":")

        # 获取小程序openid
        token = request.GET.get("token")
        openid = deCryption(token)


        # 请求微信的url
        url = order_url

        # 拿到封装好的xml数据
        body_data = get_bodyData(openid, client_ip, price)

        # 获取时间戳
        timeStamp = str(int(time.time()))

        # 请求微信接口下单
        respone = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})

        # 回复数据为xml,将其转为字典
        content = xml_to_dict(respone.content)

        if content["return_code"] == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content.get("prepay_id")
            # 获取随机字符串
            nonceStr = content.get("nonce_str")

            # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign = get_paysign(prepay_id, timeStamp, nonceStr)

            # 封装返回给前端的数据
            data = {"prepay_id": prepay_id, "nonceStr": nonceStr, "paySign": paySign, "timeStamp": timeStamp}

            return HttpResponse(json.dumps(data))

        else:
            return HttpResponse("请求支付失败")
    else:
        resp = {'code':500,'msg':"请求失败"}
        return HttpResponse(json.dumps(resp))