from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse
from hanmang import settings
from apps.users.models import UserProfile
import json
import requests
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class LoginView(View):

    @csrf_exempt
    def get(self,request,*args,**kwargs):
        code = request.GET.get('code')
        if not code:
            return HttpResponse({'msg':'缺少code','code':500})
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'\
            .format(settings.APP_ID,settings.APP_KEY,code)
        #请求微信服务器
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid'] if 'openid' in res else None
        session_Key = res['session_key'] if 'session_key' in res else None
        if not openid and not session_Key:
            return HttpResponse({'msg':'微信调用失败','code':500})
        #微信登录请求
        try:
            #获取到了openid 和 session_key
            pass
        except Exception:
            pass

        return HttpResponse({'msg':"登录失败请重试",'code':500})

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        return HttpResponse("hello post")

class UserInfoView(View):
    @csrf_exempt
    def get(self,request,*args,**kwargs):
        ## 获取用户信息 订单 评价 收藏
        return HttpResponse("hello get")

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        return HttpResponse("hello post")