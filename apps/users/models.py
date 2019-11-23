from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male","男"),
    ("female","女")
)
# Create your models here.

class BaseModel(models.Model):
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日',null = True,blank=True)
    gender = models.CharField(verbose_name='性别',choices=GENDER_CHOICES,max_length=6)
    address = models.CharField(max_length=100,verbose_name='地址',default="")
    mobile = models.CharField(max_length=11,verbose_name="手机号码")
    image = models.ImageField(verbose_name="用户头像",upload_to="head_image/%Y/%m",default="head_image/default.jpg")
    openid = models.CharField(max_length=64,db_index=True,verbose_name='openid',default=None)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username