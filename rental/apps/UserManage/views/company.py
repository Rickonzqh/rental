#coding:utf-8
'''
Created on 2019年5月5日

@author: GY071
'''

from RBAC import models as rbacmodels
from rest_framework.response import Response
from .. import serializers
from Util.page import MyPageNumberPagination
from Util.xss import xssfilter
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from .. import forms
import csv
import codecs, os
from UserManage.Functions.csv_excuter import  csv_reader


@api_view(['GET'])
def company_list(request):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    user = request.user
    key = request.GET.get('key')
    if not key:
        key=''
    if user.is_superuser:
        item_list = rbacmodels.Company.objects.filter(name__icontains = key).order_by('-id')
        item_count = item_list.count()
        pg = MyPageNumberPagination()
        item_page = pg.paginate_queryset(item_list, request,'self')
        serializer_get = serializers.CompanySerializer(instance= item_page,many=True)
        data['msg'] = 'success'
        data['count'] = item_count
        data['data'] = xssfilter(serializer_get.data)
    else:
        data['code'] = 1
        data['msg'] = '权限不足，请联系管理员'
    return Response(data)


@api_view(['POST'])
def companycreate(request):
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    user = request.user
    if user.is_superuser:
        form = forms.CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            data['code'] = 0
            data['msg'] = '创建成功'
        else:
            data['msg'] = '请检查输入'
    else:
        data['msg'] = '请检查权限'
    return Response(data)


@api_view(['POST'])
def companyupdate(request,company_id):
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    user = request.user
    if user.is_superuser:
        company_get = rbacmodels.Company.objects.filter(id = company_id).first()
        if company_get:
            form = forms.CompanyUpdateForm(request.POST)
            if form.is_valid():
                company_get.name = form.cleaned_data['name']
                company_get.address = form.cleaned_data['address']
                company_get.web = form.cleaned_data['web']
                company_get.manage = form.cleaned_data['manage']
                company_get.idcard = form.cleaned_data['idcard']
                company_get.mobilephone = form.cleaned_data['mobilephone']
                company_get.teamname = form.cleaned_data['teamname']
                company_get.teamaddress = form.cleaned_data['teamaddress']
                company_get.save()
                data['code'] = 0
                data['msg'] = '更新成功'
            else:
                data['msg'] = '请检查输入'
        else:
            data['msg'] = '参数错误'
    else:
        data['msg'] = '请检查权限'
    return Response(data)


@api_view(['GET'])
def companydelete(request,company_id):
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    user = request.user
    if user.is_superuser:
        company_get = rbacmodels.Company.objects.filter(id = company_id).first()
        if company_get:
            company_get.delete()
            data['code'] = 0
            data['msg'] = '删除成功'
        else:
            data['msg'] = '参数错误'
    else:
        data['msg'] = '请检查权限'
    return Response(data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def csv_get_example(request):
    '''

       获取csv批量上传示例
    '''
    #user = request.user
    response = HttpResponse(content_type="text/csv")
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment;filename=company_information.csv'

    writer = csv.writer(response, dialect='excel')
    rows = dict()
    rows['headers'] = ["公司名称", "机构代码", "公司地址", "官网地址", "法定代表人", "身份证号", "手机号码", "团队名称", "团队地址"]
    rows['1'] = ["某某某公司1", "GK13321", "北京XX区XX路X号", "www.XXX.com", "王XX", "100144********0224", "130****7890", "某团队1", "团队地址1"]
    rows['2'] = ["某某某公司2", "TK13321", "上海XX区XX路X号", "www.XXX.org", "李XX", "122135********0590", "130****1234", "某团队2", "团队地址2"]

    for row in rows.values():
        writer.writerow(row)
    return response


@api_view(['POST'])
def csv_upload_company(request):
    '''

    通过csv批量上传公司信息
    '''
    user = request.user
    data = {
        "code": 0,
        "msg": "",
        "data": []
    }
    if user.is_superuser:
        form = forms.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES.get('file',None)
            if csv_file:
                try:
                    f1 = open(csv_file.name, 'wb')
                    for i in csv_file.chunks():
                        f1.write(i)
                    f1.close()
                    csv_reader(csvFile=csv_file)
                    data['msg'] = '解析成功'
                except:
                    data['code'] = 1
                    data['msg'] = '文件格式不正确'
            else:
                data['code'] = 1
                data['msg'] = '参数错误'

            os.remove(csv_file.name)
        else:
            data['code'] = 1
            data['msg'] = '非法文件'
    else:
        data['code'] = 1
        data['msg'] = '权限不足'
    return Response(data)
