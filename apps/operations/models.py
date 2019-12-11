from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
from apps.users.models import BaseModel
from apps.courses.models import Course

UserProfile = get_user_model()

class UserAsk(BaseModel):
    name = models.CharField(max_length=20,verbose_name=u"姓名")
    mobile = models.CharField(max_length=11,verbose_name="手机")
    course_name = models.CharField(max_length=50,verbose_name=u"课程名")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    comments = models.CharField(max_length=200,verbose_name="评论内容")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1,"课程"),(2,"课程机构"),(3,"讲师")),default=1,verbose_name=u"收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    message = models.CharField(max_length=300,verbose_name="消息内容")
    has_read =models.BooleanField(default=False,verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name


# 用户订单表
class UserOrder(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    order_sn = models.CharField(max_length=500,null=False,verbose_name="订单编号")
    pay_price = models.DecimalField(max_digits=9,null=False,decimal_places=3,verbose_name="支付金额")
    pay_time = models.DateTimeField(null=False,verbose_name="支付时间")
    created_time = models.DateTimeField(null=False,verbose_name="订单创建时间")
    order_desc = models.CharField(null=False,max_length=300,verbose_name="订单描述")
    order_Opinion = models.CharField(null=False,max_length=800,verbose_name="订单评价")
    is_Opinion = models.BooleanField(default=False,verbose_name="是否评价")
    is_Pay = models.BooleanField(default=False,verbose_name="是否支付")

    class Meta:
        verbose_name = "用户订单"
        verbose_name_plural = verbose_name


# 用户意见
class UserOpinion(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    opinion = models.CharField(max_length=700,verbose_name="用户反馈")

    class Meta:
        verbose_name = "用户意见"
        verbose_name_plural = verbose_name