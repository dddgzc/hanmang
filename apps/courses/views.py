from django.shortcuts import render
from django.http.response import HttpResponse
from apps.courses.models import Course,CourseType,Lesson,Video,LoopItems
from apps.organizations.models import Teacher,CourseOrg
from apps.operations.models import CourseComments
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import json

# 对课程增加了分类字段
@csrf_exempt
def getCourseList(request):
    resp = {'code': -1, 'msg': '请求失败', 'data': {}}
    if request.method == 'GET':
        orgid = request.GET.get("orgid") # 课程机构
        current_page = int(request.GET.get("current_page")) #　当前第几页
        page_size = int(request.GET.get("page_size")) # 一页显示数量

        courseList = Course.objects.filter(course_org=orgid)[(current_page-1)*page_size:page_size]
        courseList = serializers.serialize("json",courseList)
        return HttpResponse(courseList)



## 获取首页轮播图
def itemsLoop(request):
    resp = {'code': -1, 'msg': '请求失败', 'data': {}}
    if request.method == 'GET':
        items = LoopItems.objects.all()
        items = serializers.serialize("json",items)
        items = json.loads(items)
        resp['data'] = items
        resp['code'] = 200
        resp['msg'] = "请求成功"
        return HttpResponse(json.dumps(resp))
    else:
        return HttpResponse(json.dumps(resp))


## 获取所有课程分类
@csrf_exempt
def getCourseType(request):
    if request.method == "GET":
        resp = {'code': -1, 'msg': '请求成功', 'data': {}}
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
        resp = {'code': 200, 'msg': '请求成功', 'data': {}}
        key = request.GET.get("key")
        course = Course.objects.filter(id = key)
        # 获取课程的第一章节
        try:
            lesson = Lesson.objects.filter(course=course[0])[0]
            vedio = Video.objects.filter(lesson = lesson)
            vedio = serializers.serialize("json", vedio)
            vedio = json.loads(vedio)
            resp['vedio'] = vedio
        except BaseException:
             pass

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
        resp = {'code': 500, 'msg': '请求失败', 'data': {}}
        return resp

## 通过分类id获取课程
@csrf_exempt
def getCourseByClassic(request):
    if request.method == "GET":
        res = {'code': 200, 'msg': '请求成功', 'data': {}}
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
        # 获取指定分类的课程的list
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

## 分页内容的统一接口
@csrf_exempt
def getPageCourses(request):
    res = {'code': -1, 'msg': '请求失败', 'data': {}}
    if request.method == "GET":
        # 当前机构
        current_origanizations_id = request.GET.get("current_origanizations_id")
        # 当前页
        current_page = int(request.GET.get("current_page"))
        # 当前分类
        current_category_id = int(request.GET.get("current_category_id"))
        # 每页显示数量
        page_size = int(request.GET.get("page_size"));

        if current_category_id == -1:
            count = Course.objects.filter(course_org=current_origanizations_id).count()
            # 计算总的页码数量
            total_page = count / page_size if count % page_size == 0 else int(count / page_size) + 1
            if current_page > total_page:
                res['code'] = 500
                res['msg'] = "暂无数据加载"
                return HttpResponse(json.dumps(res))
            courseList = Course.objects.filter(course_org=current_origanizations_id)[(current_page - 1)*page_size:current_page*page_size]
            courseList = serializers.serialize("json", courseList)
            return HttpResponse(courseList)
        else:
            q = {}
            q['current_origanizations_id'] = current_origanizations_id
            q['current_category_id'] = current_category_id
            count = Course.objects.filter(**q)

            total_page = count / page_size if count % page_size == 0 else count / page_size + 1

            if current_page > total_page:
                res['code'] = 500
                res['msg'] = "暂无数据加载"
                return HttpResponse(json.dumps(res))
            courseList = Course.objects.filter(**q)[(current_page - 1)*page_size:page_size]
            courseList = serializers.serialize("json",courseList)
            return HttpResponse(courseList)
    else:
        return HttpResponse(json.dumps(res))