# _*_ encoding:utf-8 _*_

from django.db import models

# Create your models here.

import base64
import random
import string

class EmailAccess(models.Model):
    emailname = models.CharField(verbose_name=u'账户名称', max_length=100, default="")
    emailaddr = models.CharField(verbose_name=u'邮箱地址', max_length=100, default="")
    password = models.CharField(verbose_name=u'邮箱密码', max_length=100, default="")
    host = models.CharField(verbose_name=u'邮箱主机', max_length=100, default="")
    port = models.IntegerField(verbose_name=u'端口', default=25)
    is_ssl = models.NullBooleanField(verbose_name=u'SSL端口',default=True)
    use_tls = models.NullBooleanField(verbose_name=u'启用TLS',default=True)
    subject_prefix = models.CharField(verbose_name=u'邮件前缀', max_length=200)
    status = models.NullBooleanField(verbose_name=u'启用状态', default=True)
    remark = models.CharField(verbose_name=u'备注', max_length=100, default="", null=True, blank=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __str__(self):
        return self.emailname

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 加密
        rnd_str1 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        rnd_str2 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.emailaddr = str(base64.b64encode((
                                        rnd_str1[:4]+self.emailaddr+rnd_str1[-4:]).encode('utf-8')), 'utf-8')
        self.password = str(base64.b64encode((
                                        rnd_str2[:4]+self.password+rnd_str2[-4:]).encode('utf-8')), 'utf-8')

        super(EmailAccess, self).save(force_insert, force_update, using, update_fields)
    class Meta:
        verbose_name = u'邮箱设置'
        verbose_name_plural = verbose_name

class EmailLog(models.Model):
    type = models.CharField(verbose_name=u'操作类型', max_length=50, default="")
    toaddrs = models.TextField(verbose_name=u'发送对象',  default="")
    subject = models.CharField(verbose_name=u'邮件主题', max_length=200, default="")
    content = models.TextField(verbose_name=u'邮箱内容', default="")
    attachments = models.TextField(verbose_name=u'附件列表', default="")
    status = models.NullBooleanField(verbose_name=u'操作状态', default=True)
    msg = models.CharField(verbose_name='msg', max_length=1000, default="")
    create_time = models.DateTimeField(verbose_name=u'时间', auto_now_add=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = u'邮箱日志'
        verbose_name_plural = verbose_name
