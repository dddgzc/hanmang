from django.http.response import HttpResponse
from apps.users.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from utils.Code import enCryption,deCryption
from django.core import serializers


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
        openid = WeChatOpenId.getWeChatOpenId(code=code)
        if openid is None: # 微信调用失败
            resp['code'] = -1
            resp['msg'] = '微信调用错误',
            return HttpResponse(resp)
        # 将openid 加密为token
        token = enCryption(openid=openid)
        print(type(token))
        #　获取到用户信息
        userInfo = json.loads(userInfo)
        user = UserProfile(openid=openid,nick_name=userInfo['nickName'],image=userInfo['avatarUrl'],address=userInfo['country'],username=userInfo['nickName']).save()
        # 重数据库中查询用户信息返回
        user = UserProfile.objects.filter(openid=openid).first()
        if user is None:
            resp['code'] = -1
            resp['msg'] = '未存在该用户'
            return HttpResponse(json.dumps(resp))
        resp['data'] = {
            'nickName':user.nick_name,
            'image':user.image,
            'token':token
        }

        return HttpResponse(json.dumps(resp))
    else:
        resp['code'] = 500
        resp['msg'] = "操作失败"
        return HttpResponse(json.dumps(resp))