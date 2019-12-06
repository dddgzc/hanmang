from django.shortcuts import render
from django.shortcuts import render
from django.http.response import HttpResponse
from apps.courses.models import Course
from apps.users.models import UserProfile
from apps.operations.models import UserFavorite
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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
        open_id = token.split('#')[1]  # 获取用户的openid 后期修改为高级的加密方式 现在只是一个简单的字符串拼接
        '''
            如果isCollection 是true 说明已经收藏就取消收藏
            如果isCollection 是false 说明没有收藏就收藏
        '''
        if isCollection == 'true':
            # 通过openid 查找到用户
            user = UserProfile.objects.filter(openid=open_id).first()
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
            user = UserProfile.objects.filter(openid=open_id).first()
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

@csrf_exempt
def getCollection(request):
    ## 获取未评价
    pass

@csrf_exempt
def getOrder(request):
    ## 获取所有订单
    pass

# 判断列表课程是否已经收藏
@csrf_exempt
def isFav(request):
    if request.method == "GET":
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        key = int(request.GET.get("key"))
        token = request.GET.get("token")
        open_id = token.split('#')[1]# 获取用户的openid 后期修改为高级的加密方式 现在只是一个简单的字符串拼接
        # 通过openid 查找到用户
        user = UserProfile.objects.filter(openid=open_id)[0]
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
        open_id = request.GET.get("token").split("#")[1] # 获取token 解析出openid
        # 获取用户
        user = UserProfile.objects.filter(openid=open_id)[0]
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

## 获取收藏数量
@csrf_exempt
def getFavNum(request):
    ## 获取用户的openid
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        ## 获取用户的openid
        pass
    else:
        pass

## 获取订单数量
@csrf_exempt
def getOrderNum(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        ## 获取用户的openid
        pass
    else:
        pass

##获取所有待评价数量
@csrf_exempt
def getEvaluateNum(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        ## 获取用户的openid
        pass
    else:
        pass