#coding:utf-8
'''
Created on 2019/7/13

@author: rickon
'''

from django.urls import path
from suning import views

urlpatterns = [
    path('typelist/', views.typelist, name='typelist'),
    path('goodslist/<int:type_id>/', views.goodslist, name='goodslist'),
    path('collect/<int:goods_id>/', views.collect, name='collect'),
    path('collectlist/', views.collectlist, name='collectlist'),
    path('collectdelete/<int:collect_id>/', views.collectdelete, name='collectdelete'),
]

