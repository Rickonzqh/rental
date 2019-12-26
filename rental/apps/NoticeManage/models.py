#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


class STATUS(models.Model):
    name = models.CharField(verbose_name=u'发布状态', max_length=100)
    descriptions = models.TextField(verbose_name=u'状态描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'STATUS'
        verbose_name_plural = u'文章状态'
        
class Notice(models.Model):
    title = models.CharField(verbose_name=u'通知标题', max_length=200)
    body = models.TextField(verbose_name=u'通知内容', null=True, blank=True)
    status = models.ForeignKey(STATUS, related_name='status_for_notice', on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User,related_name='notice_user',
                             verbose_name=u'创建用户', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(verbose_name=u'通知时间', default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta: 
        verbose_name = 'Notice' 
        verbose_name_plural = '通告管理'


class Message(models.Model):
    title = models.CharField(verbose_name=u'通知标题', max_length=200)
    body = models.TextField(verbose_name=u'通知内容', null=True, blank=True)
    notice = models.ForeignKey(Notice,verbose_name=u'通告',null=True, blank=True,on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name=u'阅读状态', default=False)
    url = models.CharField(verbose_name=u'通知链接', max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, related_name='message_for_user',
                             verbose_name=u'所属用户', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(verbose_name=u'通知时间', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = '通知管理'

