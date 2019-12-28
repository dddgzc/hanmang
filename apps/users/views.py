from django.http.response import HttpResponse
from apps.users.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from utils.Code import enCryption,deCryption
from django.core import serializers
from utils.WXBizDataCrypt import WXBizDataCrypt
from hanmang.settings import APP_ID

import json
from utils.Helper import getCurrentDate
from utils.WeChatOpenId import WeChatOpenId
# Create your views here.

@csrf_exempt
def getUserInfo(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":
        token = request.POST.get("token")
        openid = deCryption(token)
        try:
            user = UserProfile.objects.filter(openid=openid).first()
            if user is None:
                resp['code'] = -1
                resp['msg'] = '未存在该用户'
                return HttpResponse(json.dumps(resp))
            resp['data'] = {
                'nickName': user.nick_name,
                'image': user.image,
                'token': token
            }
            return HttpResponse(json.dumps(resp))
        except BaseException:
            pass
    else:
        pass


@csrf_exempt
def userLogin(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":
        code = request.POST.get("code")
        userInfo = request.POST.get("userInfo")
        res = WeChatOpenId.getWeChatOpenId(code=code)
        # 拿到session_key
        session_key = res['session_key']

        if res['openid'] is None: # 微信调用失败
            resp['code'] = -1
            resp['msg'] = '微信调用错误',
            return HttpResponse(resp)
        # 将openid 加密为token
        token = enCryption(openid=res['openid'])
        print(type(token))
        #　获取到用户信息
        userInfo = json.loads(userInfo)
        # 获取到用户信息之后应该判断数据库中是否存在然后存储
        # user = UserProfile(openid=openid,nick_name=userInfo['nickName'],image=userInfo['avatarUrl'],address=userInfo['country'],username=userInfo['nickName']).save()
        # 重数据库中查询用户信息返回
        user = UserProfile.objects.filter(openid=res['openid']).first()
        if user is None:
            user = UserProfile(openid=res['openid'],nick_name=userInfo['nickName'],image=userInfo['avatarUrl'],address=userInfo['country'],username=userInfo['nickName']).save()
        resp['data'] = {
            'nickName':user.nick_name,
            'image':user.image,
            'token':token,
            "session_key":session_key,
        }

        return HttpResponse(json.dumps(resp))
    else:
        resp['code'] = 500
        resp['msg'] = "操作失败"
        return HttpResponse(json.dumps(resp))


@csrf_exempt
def userPhone(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "GET":
        ency = request.GET.get("ency")
        iv = request.GET.get("iv")
        session_key = request.GET.get("session_key")
        token = request.GET.get("token")
        openid = deCryption(token)
        user = UserProfile.objects.filter(openid=openid).first()
        pc = WXBizDataCrypt(appId=APP_ID,sessionKey=session_key)
        user.mobile = pc['phoneNumber']
        user.save()
        print(pc['phoneNumber'])
        resp = {'code':200,'msg':'操作成功','data':{}}
        return HttpResponse(json.dumps(resp))
    else:
        resp['code'] = 500;
        resp['msg'] = "操作失败"
        return HttpResponse(json.dumps(resp))