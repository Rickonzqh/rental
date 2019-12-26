#coding:utf-8

# Create your models here.

from django.db import models

# Create your models here.

class CaptchaCode(models.Model):

    code = models.CharField(verbose_name=u'验证码', max_length=100, default="")
    key = models.CharField(verbose_name=u'校验码', max_length=200, default="")
    create_time = models.DateTimeField(verbose_name=u'生成时间', auto_now_add=True)
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = u'仓库管理'
        verbose_name_plural = verbose_name
