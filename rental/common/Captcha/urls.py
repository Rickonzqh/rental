#coding:utf-8
'''
Created on 2019/4/21

@author: rickon
'''

from django.urls import path
from . import views

urlpatterns = [
    path('captcha/<str:key>/', views.create_captcha, name='create_captcha'),
]

