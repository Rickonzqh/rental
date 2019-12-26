#coding:utf-8
'''
Created on 2018年10月29日

@author: 
'''

from django import forms
from django.forms import ModelForm
from RBAC import models as rbacmodels

class UserCreateForm(forms.Form):
    username = forms.CharField(label='账号',max_length=75)
    email = forms.EmailField(label='密码')
    mobilephone = forms.CharField(label='手机号码')
    #department = forms.CharField(label='部门',max_length=75)
    area = forms.CharField(label='区域',max_length=75)
    roles = forms.CharField(label='角色',max_length=75)
    companykey = forms.CharField(label='企业',max_length=75)
    
    
    
class UserProfile(ModelForm):
    class Meta:
        model  = rbacmodels.Profile
        fields= ('mobilephone','description','roles')


class UploadForm(forms.Form):
    file = forms.FileField()


class CompanyForm(ModelForm):
    class Meta:
        model  = rbacmodels.Company
        fields= ('name','key','address','web','manage','idcard','mobilephone','teamname','teamaddress')
        
class CompanyUpdateForm(ModelForm):
    class Meta:
        model  = rbacmodels.Company
        fields= ('name','address','web','manage','idcard','mobilephone','teamname','teamaddress')