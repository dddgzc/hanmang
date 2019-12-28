from django.core import serializers
from apps.organizations.models import CourseOrg
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.


@csrf_exempt
def getOrganizations(request):
    # 获取组织 所有公司
    if request.method == 'POST':
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        all_class = CourseOrg.objects.all()
        all_class = serializers.serialize("json", all_class)
        all_class = json.loads(all_class)
        resp['data'] = all_class
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        resp['code'] = '-1';
        resp['msg'] = 'error request use post'
        return HttpResponse(json.dumps(resp))

