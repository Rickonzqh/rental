# coding:utf-8
from django.db import models

# Create your models here.

class Grid(models.Model):
    name = models.CharField(verbose_name=u'网格名称', max_length=100, default="")
    manager = models.CharField(verbose_name=u'格长id', max_length=30, default='')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'网格'
        verbose_name_plural = verbose_name


class Hao(models.Model):
    grid = models.ForeignKey(Grid, verbose_name=u'网格', null=True, blank=True)
    newnum = models.IntegerField(verbose_name=u'新增放号量', default=0)
    newnum58 = models.IntegerField(verbose_name=u'新增58+规模', default=0)
    newnum58reg = models.FloatField(verbose_name=u'新增58+下单登记率', default=0.0)
    chargerate = models.FloatField(verbose_name=u'首充率', default=0.0)
    trans4g = models.FloatField(verbose_name=u'4G转化率', default=0.0)
    month = models.CharField(verbose_name=u'数据月份', max_length=10, default='')
    create_time = models.DateTimeField(verbose_name=u'时间', auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'放号精准拉新'
        verbose_name_plural = verbose_name

