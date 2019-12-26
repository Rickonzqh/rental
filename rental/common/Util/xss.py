#coding:utf-8
'''
Created on 2019/7/10

@author: rickon
'''
from django.utils.html import escape

# xss过滤
def xssfilter(data):
    if isinstance(data,list):
        for k in data:
            k=xssfilter(k)
    elif isinstance(data,dict):
        for k,value in data.items():
            data[k]=xssfilter(value)
    else:
        data=escape(data)
    return data

