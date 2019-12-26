#coding:utf-8
from django.contrib.auth.models import User
from rest_framework.response import Response
from .. import serializers
from rest_framework.decorators import api_view
from RBAC import models
from ..Functions import select
from RBAC.serializers.serializers import RoleSerializer
from .. import forms
import hashlib
import datetime
from django.contrib.auth.hashers import make_password 
from Util.check import checphone
from Framework.settings import JWT_KEY
from UserManage.Functions import user_email
from django.db.models import  Q
from Util.many2many import many_many_addall
from Util.page import MyPageNumberPagination
from Util.xss import xssfilter

# Create your views here.
@api_view(['GET'])
def user_list(request):
    user = request.user
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    key = request.GET.get('key')
    if not key:
        key=''
    if user.is_superuser:
        user_list = User.objects.filter(Q(username__icontains = key)|
                                        Q(email__icontains = key),
                                        is_superuser=False
                                        ).order_by('is_active','-date_joined')
        user_count = user_list.count()
        pg = MyPageNumberPagination()
        user_page = pg.paginate_queryset(user_list, request,'self')
        serializer_get = serializers.UserManageSerializer(instance= user_page,many=True)
        data['msg'] = 'success'
        data['count'] = user_count
        data['data'] = xssfilter(serializer_get.data)
    else:
        data['code'] = 1
        data['msg'] = '权限不足，请联系管理员'
    return Response(data)


@api_view(['GET'])
def user_details_select_input(request,argu='department'):
    user = request.user
    json_data = {
          "code": 1
          ,"msg": ""
          ,"data":[]
        }
    if user.is_superuser:
        if argu == 'department':
            json_data['code'] = 0
            department_lists = models.Department.objects.filter(parent__isnull=True)
            department_select = select.departmentselecttotree(department_lists)
            json_data['data']=xssfilter(department_select)
        elif argu =='area':
            json_data['code'] = 0
            area_lists = models.Area.objects.filter(parent__isnull=True)
            area_select = select.areaselecttotree(area_lists)
            json_data['data']=xssfilter(area_select)
        else:
            json_data['msg']='参数不合法'
    else:
        json_data['msg']='权限不足'
    return Response(json_data)

@api_view(['GET'])
def roleslist(request):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    user=request.user
    key = request.GET.get('key')
    if not key:
        key=''
    if user.is_superuser:
        role_list = models.Role.objects.all().order_by('-id')
        role_count = role_list.count()
        pg = MyPageNumberPagination()
        user_page = pg.paginate_queryset(role_list, request,'self')
        serializers = RoleSerializer(instance= user_page,many=True)
        data['msg'] = 'success'
        data['count'] = role_count
        data['data'] = xssfilter(serializers.data)
    else:
        data['code'] = 1
        data['msg'] = '无权访问'
    return Response(data)

@api_view(['POST'])
def user_create(request):
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    form = forms.UserCreateForm(request.POST)
    user = request.user
    if user.is_superuser:
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            mobilephone=form.cleaned_data['mobilephone']
            #department=form.cleaned_data['department']
            area=form.cleaned_data['area']
            roles=form.cleaned_data['roles']
            company_key = form.cleaned_data['companykey']
            company_get = models.Company.objects.get_or_create(key=company_key)[0]
            user_roles_list = models.Role.objects.filter(id__in = roles.split(','))
            if checphone(mobilephone):
                res = User.objects.get_or_create(
                    username=username,
                    )
                if res[1]:
                    #此处添加邮件发送代码
                    user_get = res[0]
                    user_get.email=email
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email+JWT_KEY+str(datetime.datetime.now())).encode('utf-8'))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                            email=email,
                            urlarg=urlarg,
                            is_start=True,
                            user = user_get,
                            )
                    #user.profile.department=models.Department.objects.filter(id=department).first()
                    user_get.profile.area = models.Area.objects.filter(id = area).first()
                    user_get.profile.mobilephone = mobilephone
                    #user_get.profile.company = company_get
                    user_get.is_active = False
                    user_get.save()
                    user = many_many_addall(user_get,user_get.profile.roles,user_roles_list)
                    try:
                        res = user_email.sendregistmail(username,email,urlarg)
                    except:
                        res=False
                    if res:
                        company_get.user = user_get
                        company_get.save()
                        data['code'] = 0
                        data['msg'] = '密码重置邮件已发送'
                    else:
                        user.delete()
                        data['msg'] = '邮件发送失败，请检查邮箱设置'
                else:
                    data['msg'] = '邮箱或用户名已注册'
            else:
                data['msg'] = '手机号不合法'
        else:
            data['msg'] = '请检查输入'
    else:
        data['msg'] = '无权访问'
    return Response(data)
        


@api_view(['GET'])
def user_action(request,action,user_id):
    user = request.user
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    if user.is_superuser:
        user_get = User.objects.filter(id= user_id).first()
        if user_get and user_get.is_superuser==False:
            if user_get.is_active and action=='deny':
                user_get.is_active=False
            elif not user_get.is_active and action=='access':
                user_get.is_active=True
            user_get.save()
            data['code'] = 0
            data['msg'] = '操作成功'
        else:
            data['msg'] = '所选用户不存在或所选用户为特殊用户'
    else:
        data['msg'] = '权限错误'
    return Response(data)  
    

@api_view(['GET'])
def user_delete(request,user_id):
    user = request.user
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    if user.is_superuser:
        user_get = User.objects.filter(id= user_id).first()
        if user_get and user_get.is_superuser==False:
            user_get.delete()
            data['code'] = 0
            data['msg'] = '操作成功'
        else:
            data['msg'] = '所选用户不存在或所选用户为特殊用户'
    else:
        data['msg'] = '权限错误'
    return Response(data)



@api_view(['POST'])
def user_update(request,user_id):
    user = request.user
    data = {
      "code": 1,
      "msg": "",
      "count": '',
      "data": []
    }
    if user.is_superuser:
        user_get = User.objects.filter(id= user_id).first()
        if user_get and user_get.is_superuser==False:
            form = forms.UserCreateForm(request.POST)
            if form.is_valid():
                user_get.profile.mobilephone = form.cleaned_data['mobilephone']
                user_get.profile.description = form.cleaned_data['description']
                user_get.save()
                roles=form.cleaned_data['roles']
                user_roles_list = models.Role.objects.filter(id__in = roles.split(','))
                user = many_many_addall(user,user.profile.roles,user_roles_list)
                data['code'] = 0
                data['msg'] = '操作成功'
            else:
                data['msg'] = '请检查输入'
        else:
            data['msg'] = '所选用户不存在或所选用户为特殊用户'
    else:
        data['msg'] = '权限错误'
    return Response(data)
