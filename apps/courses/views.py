from django.shortcuts import render
from django.http.response import HttpResponse
from apps.courses.models import Course,CourseType
from apps.organizations.models import Teacher,CourseOrg
from apps.operations.models import CourseComments
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import json

# Create your views here.
# 课程机构下的所有老师的所有课程
# 1. orgid 机构id
# 2. 通过机构id 获取机构下所有老师
# 3. 获取所有老师的所有课程
@csrf_exempt
def courseList(request):
    if request.method == 'GET':
        resp = {'code': -1, 'msg': '请求失败', 'data': {}}
        orgid = request.GET.get('orgid')
        teachers = Teacher.objects.filter(org=orgid)
        courseList = []

        for teacher in teachers:
            courses = Course.objects.filter( teacher=teacher.id )
            for course in courses:
                courseList.append(course)

        courseList = serializers.serialize("json",courseList)
        print(type(courseList))
        return HttpResponse(courseList)


## 获取所有课程分类
@csrf_exempt
def getCourseType(request):
    if request.method == "GET":
        resp = {'code': -1, 'msg': '请求失败', 'data': {}}
        courseType = CourseType.objects.all()
        courseType = serializers.serialize("json",courseType)
        courseType = json.loads(courseType)
        resp['data'] = courseType
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': -1, 'msg': '请求失败', 'data': {}}
        return HttpResponse(json.dumps(resp))

# 指定课程的内容
# key 为课程id
@csrf_exempt
def getCourse(request):
    if request.method == "GET":
        resp = {'code': -1, 'msg': '请求失败', 'data': {}}
        key = request.GET.get("key")
        course = Course.objects.filter(id = key)
        if course is None:
            resp['msg'] = "课程暂未开发";
            return HttpResponse(json.dumps(resp))
        course = serializers.serialize("json",course)
        course = json.loads(course)
        resp['code'] = 200
        resp['msg'] = "请求成功"
        resp['data'] = course
        return HttpResponse(json.dumps(resp))
    else:
        resp = {'code': -1, 'msg': '请求失败', 'data': {}}
        return resp

## 通过分类id获取课程
@csrf_exempt
def getCourseByClassic(request):
    if request.method == "GET":
        res = {'code': -1, 'msg': '请求失败', 'data': {}}
        # 当前机构 id
        orgid = int(request.GET.get("orgid"))
        # 选择分类 id
        classic = int(request.GET.get("classic"))
        # 获取当前机构下所有老师
        teachers = Teacher.objects.filter(org=orgid)
        # 获取所有老师的所有课程
        courseList = []
        for teacher in teachers:
            courses = Course.objects.filter(teacher=teacher.id)
            for course in courses:
                courseList.append(course)
        # 所有课程的list
        if classic == -1:
            courseList = serializers.serialize("json",courseList)
            return HttpResponse(courseList)
        else:
        # 获取指定分类的课程
            courseClassicList = []
            for course in courseList:
                if(course.category_id == int(classic)):
                    courseClassicList.append(course)

            courseClassicList = serializers.serialize("json",courseClassicList)
            return HttpResponse(courseClassicList)
    else:
        res = {'code': -1, 'msg': '请求失败', 'data': {}}
        return HttpResponse(json.dumps(res))


##获取当前课程的评价
@csrf_exempt
def getCourseComment(request):
    if request.method == "GET":
        res = {'code': -1, 'msg': '请求失败', 'data': {}}
        key = request.GET.get("key")
        ## 获取当前课程
        course = Course.objects.filter(id = key).first()
        ## 获取当前课程的所有评价
        allComments = CourseComments.objects.filter(course=course)
        allComments = serializers.serialize("json",allComments)
        allComments = json.loads(allComments)
        res['code'] = 200
        res['msg'] = '请求失败'
        res['data'] = allComments
        return HttpResponse(json.dumps(res))
    else:
        res = {'code': -1, 'msg': '请求失败', 'data': {}}
        return HttpResponse(json.dumps(res))