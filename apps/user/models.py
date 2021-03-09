from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, default='', verbose_name="昵称")
    image = models.ImageField(upload_to="static/image/%Y/%m", max_length=100, default=u"/static/image/zwj_z5URuSP.png")

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nick_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'邮箱验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name='验证类型', choices=(("register", u"注册"), ("forget", u'找回密码')), max_length=10)
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class TemporaryUser(models.Model):
    username = models.CharField(max_length=20, default='', verbose_name="名称", unique=True)
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    add_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = '临时用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
