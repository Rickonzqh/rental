#coding:utf-8
'''
Created on 2019/5/19

@author: rickon
'''

from django.urls import path
from . import views

urlpatterns = [
    path('noticelist/', views.noticelist, name='noticelist'),
    path('getnotice/<str:noticeid>/', views.getnotice, name='getnotice'),
    path('savenotice/', views.savenotice, name='savenotice'),
    path('noticedelete/<str:noticeid>/', views.noticedelete, name='noticedelete'),
    path('noticeaudit/<str:noticeid>/<str:action>/', views.noticeaudit, name='noticeaudit'),

    path('messagelist/', views.messagelist, name='messagelist'),
    path('unreadmessagelist/', views.unreadmessagelist, name='unreadmessagelist'),
    path('readallmessage/', views.readallmessage, name='readallmessage'),
    path('getmessage/<str:messageid>/', views.getmessage, name='getmessage'),
    path('messagedelete/<str:messageid>/', views.messagedelete, name='messagedelete'),
]

