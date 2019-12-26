#coding:utf-8
'''
Created on 2019年4月30日

@author: GY071
'''
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .. import models,forms
from ..serializers import serializers as rbacserializers
from Util.xss import xssfilter


@api_view(['POST'])
def companyupdate(request):
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    user = request.user
    item_get = models.Company.objects.filter(user=user).first()
    if item_get:
        form = forms.CompanyForm(request.POST)
        if form.is_valid():
            item_get.name=form.cleaned_data['name']
            #item_get.key=form.cleaned_data['key']
            item_get.address=form.cleaned_data['address']
            item_get.manage=form.cleaned_data['manage']
            item_get.idcard=form.cleaned_data['idcard']
            item_get.mobilephone=form.cleaned_data['mobilephone']
            item_get.teamname=form.cleaned_data['teamname']
            item_get.teamaddress=form.cleaned_data['teamaddress']
            item_get.save()
            data['msg'] = '企业信息更新成功'
            data['code'] = 0
        else:
            data['msg'] = '请检查输入'
    else:
        data['msg'] = '请检查权限'
    return Response(data)


@api_view(['GET'])
def companydetails(request):
    data = {
      "code": 1,
      "msg": "",
      "data": []
    }
    user = request.user
    item_get = models.Company.objects.get_or_create(user=user)
    if item_get:
        item_get=item_get[0]
        data_get = rbacserializers.CompanySerializer(instance= item_get)
        data['code'] = 0
        data['data'] = xssfilter(data_get.data)
    else:
        data['msg'] = '请检查权限'
    return Response(data)