#coding:utf-8
'''
Created on 2019/7/10

@author: rickon
'''

#多对多批量添加
def many_many_addall(model_get,argv,queryset_list_get):
    for queryset_get in queryset_list_get:
        argv.add(queryset_get)
    return model_get

#多对多批量删除
def many_many_removeall(model_get,argv,queryset_list_get):
    for queryset_get in queryset_list_get:
        argv.remove(queryset_get)
    return model_get
