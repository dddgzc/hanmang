from django.http.response import HttpResponse
from apps.users.models import UserProfile
from django.views.decorators.csrf import csrf_exempt

import json

from utils.Helper import getCurrentDate

from utils import WeChatOpenId

# Create your views here.

@csrf_exempt
def login(request):
    '''
    1. 如果数据库中有这个open_id 直接获取数据就好了
    2. 如果没有就保存 并且把用户信息保存起来
    :param request:
    :return:
    '''
    if request.method == 'POST':
        resp = {'code':200,'msg':'操作成功','data':{}}

        code = request.POST.get('code')

        if not code:
            resp['code'] = -1
            resp['msg'] = '需要code'
            return HttpResponse(resp)

        openid = WeChatOpenId.WeChatOpenId.getWeChatOpenId(code=code)
        if openid is None:
            resp['code'] = -1
            resp['msg'] = '微信调用错误',
            return HttpResponse(resp)


        nickname = request.POST['nickName'] if 'nickName' in request.POST else ''
        sex = request.POST['gender'] if 'gender' in request.POST else 0
        avatar = request.POST['avatarUrl'] if 'avatarUrl' in 'avatarUrl' in request.POST else ''

        user = UserProfile.objects.filter(openid=openid).first()
        # 判断是否已经注册过
        if not user:
            user = UserProfile(nick_name=nickname,gender=sex,image=avatar,openid=openid,salt=WeChatOpenId.WeChatOpenId.geneSalt())
            user.save()
        user_info = UserProfile.objects.filter(openid=openid).first()
        # 生成token
        token = "%s#%s" %(WeChatOpenId.WeChatOpenId.geneAuthCode(user_info),user_info.openid)
        resp['data'] = {'token':token}
        return HttpResponse(json.dumps(resp))
    elif request.method == 'GET':
        return HttpResponse({'msg':'使用post请求','code':500})

@csrf_exempt
def checkreg(request):
    pass

@csrf_exempt
def getUserInfo(request):
    #通过token 获取用户信息
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    token = request.POST.get('token')
    if token is None or token == '':
        resp['code'] = -1
        resp['msg'] = '操作失败 请先登陆'
        return HttpResponse(json.dumps(resp))

    open_id = token.split('#')[1]
    user = UserProfile.objects.filter(openid=open_id).first()
    if user is None:
        resp['code'] = -1
        resp['msg'] = '未存在该用户'
        return HttpResponse(json.dumps(resp))

    resp['data'] = {
        'nickName':user.nick_name,
        'image':user.image
    }

    return HttpResponse(json.dumps(resp))

@csrf_exempt
def getAllCollection(request):
    if request.method == 'GET':
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        return HttpResponse(json.dumps(resp))

def test(request):
    if request.method == 'GET':
        return HttpResponse("test successful")