#coding:utf-8
'''
Created on 2018年10月29日

@author: 残源
'''
from django.urls import path
from .views import views,Company

urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('session/',views.session,name='session'),
    path('resetpsd/',views.resetpsd,name='resetpsd'),
    path('infomain/',views.info_main,name='infomain'),
    path('menu/',views.getmenu,name='getmenu'),
    
    path('companydetails/',Company.companydetails,name='companydetails'),
    path('companyupdate/',Company.companyupdate,name='companyupdate'),
    
    path('forgetpsd/',views.forgetpsd,name='forgetpsd'),
    path('forgetchangepsd/',views.forgetchangepsd,name='forgetchangepsd'),
    
    path('registinit/',views.registinit,name='registinit'),
    ]