#coding:utf-8
'''
Created on 2019/5/1

@author: rickon
'''

from django.urls import path
from . import views

urlpatterns = [

    path('test/', views.test, name='test'),
]
