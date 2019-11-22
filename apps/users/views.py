from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse
from hanmang import settings
from apps.users.models import UserProfile
import json
import requests


# Create your views here.
class LoginView(View):
    def get(self,request,*args,**kwargs):
        pass
    #微信登陆请求
    def post(self,request,*args,**kwargs):
        code = request.data.get('code')
        if not code:
            return HttpResponse({'message':'缺少code','code':500})

        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(settings.APP_ID,settings.APP_KEY,code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid'] if 'openid' in res else None
        if not openid:
            return HttpResponse({'message':'微信调用失败','code':500})
        # 判断是否是第一次登陆
        try:
            user = UserProfile.objects.get(openid=openid)
        except Exception:
            # 不存在保存到user中
            pass