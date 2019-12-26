#coding:utf-8
'''
Created on 2018年10月29日

@author: 
'''

from django import forms
from django.forms import ModelForm
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(label='账号',max_length=75)
    password = forms.CharField(label='密码',max_length=25)
    vercode = forms.CharField(label='验证码',max_length=25)
    captchakey = forms.CharField(label='验证码key', max_length=200)
    
class ResetpsdForm(forms.Form):
    oldpassword = forms.CharField(label='原始密码',max_length=25)
    newpassword = forms.CharField(label='新密码',max_length=25)
    repassword = forms.CharField(label='重复密码',max_length=25)
    
class ForgetForm(forms.Form):
    email = forms.EmailField(label='账号')
    username = forms.CharField(label='登陆账号',max_length=75)
    vercode = forms.CharField(label='验证码', max_length=25)
    captchakey = forms.CharField(label='验证码key', max_length=200)

class ForgetChangeForm(forms.Form):
    email = forms.EmailField(label='账号')
    checkcode = forms.CharField(label='校验码',max_length=200)
    newpassword = forms.CharField(label='新密码',max_length=25)
    repassword = forms.CharField(label='重复密码',max_length=25)
    
class RegistinitForm(forms.Form):
    #username = forms.CharField(label='用户昵称',max_length=200)
    email = forms.EmailField(label='账号')
    checkcode = forms.CharField(label='校验码',max_length=200)
    password = forms.CharField(label='新密码',max_length=25)
    repass = forms.CharField(label='重复密码',max_length=25)
    vercode = forms.CharField(label='验证码', max_length=25)
    captchakey = forms.CharField(label='验证码key', max_length=200)
    
    
class CompanyForm(ModelForm):
    class Meta:
        model  = models.Company
        fields= ('name','address','web','manage','idcard','mobilephone','teamname','teamaddress')