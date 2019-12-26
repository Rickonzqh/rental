#coding:utf-8
'''
Created on 2018年11月2日

@author: 残源
'''


from django.urls import path
from UserManage.views import views,company
urlpatterns = [
    path('userlist/',views.user_list,name='user_list'),
    path('usercreate/',views.user_create,name='usercreate'),
    path('userdelete/<str:user_id>/',views.user_delete,name='user_delete'),
    path('user_update/<str:user_id>/',views.user_update,name='user_update'),
    path('roleslist/',views.roleslist,name='roleslist'),
    path('select/<str:argu>/',views.user_details_select_input,name='user_details_select_input'),
    
    path('usersction/<str:action>/<int:user_id>/',views.user_action,name='usersction'),
    
    
    path('companylist/',company.company_list,name='company_list'),
    path('companycreate/',company.companycreate,name='companycreate'),
    path('companyupdate/<str:company_id>/',company.companyupdate,name='companyupdate'),
    path('companydelete/<str:company_id>/',company.companydelete,name='companydelete'),
    path('csv_get_example/',company.csv_get_example,name='csv_get_example'),
    path('csv_upload_company/',company.csv_upload_company,name='csv_upload_company'),
    ]