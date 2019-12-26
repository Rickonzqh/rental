#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 商品分类
class Type(models.Model):
    is_root = models.BooleanField(verbose_name=u'商品分类', default=False)
    name = models.CharField(verbose_name=u'类名', max_length=100)
    descriptions = models.TextField(verbose_name=u'评测描述', null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name=u'上级分类', blank=True, null=True,
                               on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = u'商品分类'


class Goods(models.Model):
    name = models.TextField(verbose_name=u'商品名称')
    sku = models.CharField(verbose_name=u'sku', max_length=20)
    type = models.ForeignKey(Type, verbose_name='分类', related_name='goods_type',on_delete=models.SET_NULL,null=True,blank=True)
    type1 = models.CharField(verbose_name=u'类别1', max_length=30, null=True,blank=True)
    type2 = models.CharField(verbose_name=u'类别2', max_length=30, null=True, blank=True)
    type3 = models.CharField(verbose_name=u'类别3', max_length=30, null=True, blank=True)
    price = models.FloatField(verbose_name=u'价格', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Goods'
        verbose_name_plural = u'商品名称'


class Collect(models.Model):
    name = models.TextField(verbose_name=u'商品名称')
    sku = models.CharField(verbose_name=u'sku', max_length=20)
    type1 = models.CharField(verbose_name=u'类别1', max_length=30, null=True,blank=True)
    type2 = models.CharField(verbose_name=u'类别2', max_length=30, null=True, blank=True)
    type3 = models.CharField(verbose_name=u'类别3', max_length=30, null=True, blank=True)
    price = models.FloatField(verbose_name=u'价格', null=True)
    user = models.ForeignKey(User, verbose_name=u'人员关联', related_name='suning_collect', on_delete=models.CASCADE, )
    create_time = models.DateTimeField(verbose_name=u'收藏时间', auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Collect'
        verbose_name_plural = u'商品收藏'
