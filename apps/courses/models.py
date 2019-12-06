from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.
"""
    实体1 <关系> 实体2
    课程 章节 视频 课程资源
    course  课程
    Lesson  章节
    video   视频
    CourseResource 课程资源
"""
#2.实体具体的字段

#3.每一个字段的类型 是否必填
class CourseType(BaseModel):
    type = models.CharField(max_length=100,verbose_name="课程类型")
    desc = models.CharField(max_length=200,verbose_name=u"类型描述")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "类型名"
        verbose_name_plural = verbose_name

class Course(BaseModel):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name="讲师")
    name = models.CharField(verbose_name="课程名",max_length=50)
    desc = models.CharField(verbose_name="课程描述",max_length=300)
    ## 课程价格
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0.0,verbose_name="课程价格")
    learn_times = models.IntegerField(default=0,verbose_name="学习时长(分钟数)")
    degree = models.CharField(verbose_name="难度",choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2)
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    category = models.ForeignKey(CourseType,on_delete=models.CASCADE,verbose_name=u"课程分类")
    tag = models.CharField(default="",verbose_name="课程标签",max_length=10)
    youneed_know = models.CharField(default="",max_length=300,verbose_name="课程须知")
    teacher_tell = models.CharField(default="",max_length=300,verbose_name="老师告诉你")
    detail = UEditorField(verbose_name="课程详情",height=300,width=600,imagePath='course/uediter/',filePath="course/ueditor/files/",default="")
    image = models.ImageField(upload_to="course/%Y/%m",verbose_name="封面图",max_length=100)

    style_fields = {
        "detail":"ueditor"
    }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name


class Lesson(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE) #on_delete 表示对应的外键数据被删除后当前数据应该怎么办
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    learn_times = models.IntegerField(default=0,verbose_name=u"学习时长(分钟)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson,verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="视频名")
    learn_times = models.IntegerField(default=0,verbose_name=u"学习时长(分钟数)")
    url = models.CharField(max_length=200,verbose_name=u"访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
