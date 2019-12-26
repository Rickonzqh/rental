#coding:utf-8
'''
Created on 2019/5/15

@author: rickon
'''

from . import models
from django.forms import ModelForm


class Noticeform(ModelForm):
    class Meta:
        model = models.Notice
        fields = ['title', 'body']


