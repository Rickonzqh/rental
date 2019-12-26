#coding:utf-8
'''
Created on 2018年11月2日

@author: 残源
'''


from django.urls import path
from . import views

urlpatterns = [
    path('loglist/',views.Log_list,name='loglist'),
    ]