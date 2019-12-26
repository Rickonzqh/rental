#coding:utf-8
'''
Created on 2019/7/13

@author: rickon
'''

from .. import models

# 递归当前分类下所有分类
def type2type(type_obj):
    type_list = models.Type.objects.filter(parent=type_obj)
    for item in type_list:
        list_get = type2type(item)
        type_list = type_list | list_get
    return type_list

