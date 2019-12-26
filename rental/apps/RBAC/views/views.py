 #coding:utf-8
#from rest_framework.response import Response
from django.http import JsonResponse
from ..Functions.jwttoken import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
import django.utils.timezone as timezone
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from Util.check import checkpsd
from LogManage.views import createLog
from LogManage.models import Log
from django.contrib import auth
from .. import forms,models
from ..Functions import menu
import datetime
import hashlib
from django.contrib.auth.hashers import make_password 
from Framework.settings import JWT_KEY
from UserManage.Functions import user_email
from django.utils.html import escape
from Captcha.views import check_captcha


cur_date = datetime.datetime.now().date()
# Create your views here.

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    json_data = {
      "code": 1
      ,"msg": ""
      ,"data": {
      }
    }
    log={
        'type':'账号操作',
        'user':'',
        'action':'用户登陆',
        'status':False,
    }
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        vercode = form.cleaned_data['vercode']
        captchakey = form.cleaned_data['captchakey']
        if check_captcha(captchakey,vercode):
            user_get = User.objects.filter(username=username).first()
            if user_get:
                log['user']=user_get
                if user_get.profile.lock_time > timezone.now():
                    json_data['msg'] = u'账号已锁定,'+str(user_get.profile.lock_time.strftime("%Y-%m-%d %H:%M"))+'后可尝试'
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user:
                        user.profile.error_count = 0
                        user.profile.login_count += 1
                        user.save()
                        token = MyTokenObtainPairSerializer.get_token(user)
                        json_data['code'] = 0
                        json_data['msg'] = '登陆成功'
                        json_data['data']['access_token'] = token
                        json_data['data']['deny'] = user.is_superuser
                        log['status']=True
                    else:
                        user_get.profile.error_count += 1
                        if  user_get.profile.error_count >= 5:
                            user_get.profile.error_count=0
                            user_get.profile.lock_time = timezone.now()+datetime.timedelta(minutes=10)
                        user_get.save()
                        json_data['msg']  = '登陆失败,已错误登录'+str(user_get.profile.error_count) +'次,5次后账号锁定'
                log['action']=log['action']+json_data['msg']
                createLog(log)
            else:
                json_data['msg']  = '请检查用户信息'
        else:
            json_data['msg'] = '验证码不正确,请重试'
    else:
        json_data['msg']  = '请检查输入'
    return JsonResponse(json_data)


@api_view(['GET'])
def info_main(request):
    user = request.user
    data = {
              "code": 0
              ,"msg": "information"
              ,"data": {
                "login_count": user.profile.login_count
                ,'log_count':0
                ,'download_count':0
              }
            }
    return JsonResponse(data)



@api_view(['GET'])
def session(request):
    user = request.user
    data = {
              "code": 0
              ,"msg": "selfinformation"
              ,"data": {
                "username": escape(user.username)
              }
            }
    return JsonResponse(data)

@api_view(['GET'])
def logout(request):
    json_data = {
      "code": 1
      ,"msg": ""
      ,"data": {
      }
    }
    json_data['code'] = 0
    json_data['msg']  = '注销成功'
    json_data['data'] = []
    
    return JsonResponse(json_data)



@api_view(['POST'])    
def resetpsd(request):
    user = request.user
    data = {
          "code": 1
          ,"msg": ""
          ,"data": {
              'status':'false'
              ,'token':''}
        }
    log={
        'type':'账号操作',
        'user':user,
        'action':'用户注销',
        'status':False,
    }
    if request.method == 'POST':
        form = forms.ResetpsdForm(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data['oldpassword']
            newpassword = form.cleaned_data['newpassword']
            repassword = form.cleaned_data['repassword']
            if checkpsd(newpassword):
                if newpassword and newpassword==repassword:
                    if oldpassword:
                        user = auth.authenticate(username = user.username,password = oldpassword)
                        if user:
                            user.set_password(newpassword)
                            user.save()
                            auth.logout(request)
                            data['code'] = 0
                            data['data']['status']  = 'true'
                            data['msg']  = '重置成功，请重新登陆'
                            log['status']=True
                        else:
                            data['msg']  = '请检查原始密码'
                    else:
                        data['msg']  = '请检查原始密码'
                else:
                    data['msg']  = '两次密码不一致'
            else:
                data['msg']  = '密码不符合安全规范'
            createLog(log)
        else:
            data['msg']  = '请检查输入'
    else:
        data['msg']  = '请求方式错误'
    return JsonResponse(data,safe=False)


@api_view(['POST'])
@permission_classes((AllowAny,))
def forgetpsd(request):
    json_data = {
      "code": 1
      ,"msg": ""
      ,"data": {
      }
    }
    form = forms.ForgetForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        vercode = form.cleaned_data['vercode']
        captchakey = form.cleaned_data['captchakey']
        if check_captcha(captchakey, vercode):
            user = User.objects.filter(email = email,username=username).first()
            if user:
                count_num = models.UserResetpsd.objects.filter(email = email,is_check=False,user=user,updatetime__gte=cur_date - datetime.timedelta(days=1)).count()
                if count_num <= 5:
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email+JWT_KEY+str(datetime.datetime.now())).encode('utf-8'))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                        email=email,
                        urlarg=urlarg,
                        user = user,
                        )
                    res = user_email.sendresetpsdmail(email,urlarg)
                    if res:
                        json_data['code'] = 0
                        json_data['msg'] = '邮件发送成功，请检查邮件'
                    else:
                        json_data['msg'] = '邮件发送失败，请联系管理员'
                else:
                    json_data['msg'] = '重置次数过多，请检查邮箱'
            else:
                json_data['msg'] = '用户信息有误,请重试'
        else:
            json_data['msg'] = '验证码不正确,请重试'
    else:
        json_data['msg'] = '请检查输入'
    return JsonResponse(json_data)
               
@api_view(['POST'])
@permission_classes((AllowAny,))
def forgetchangepsd(request):
    json_data = {
      "code": 1
      ,"msg": ""
      ,"data": {
      }
    }
    form = forms.ForgetChangeForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        checkcode = form.cleaned_data['checkcode']
        newpassword = form.cleaned_data['newpassword']
        repassword = form.cleaned_data['repassword']
        UserResetpsd_get = models.UserResetpsd.objects.filter(email = email,is_start=False,urlarg=checkcode,is_check=False,updatetime__gte=cur_date - datetime.timedelta(days=1)).first()
        if UserResetpsd_get:
            user= UserResetpsd_get.user
            if checkpsd(newpassword):
                if newpassword and newpassword==repassword:
                    user.set_password(newpassword)
                    user.save()
                    UserResetpsd_get.is_check=True
                    UserResetpsd_get.save()
                    json_data['code'] = 0
                    json_data['msg']  = '重置成功，请重新登陆'
                else:
                    json_data['msg']  = '两次密码不一致'
            else:
                json_data['msg']  = '密码不符合安全规范'
        else:
            json_data['msg']  = '校验信息有误，系统已记录错误信息'
    else:
        json_data['msg'] = '请检查输入'
    return JsonResponse(json_data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def registinit(request):
    json_data = {
      "code": 1
      ,"msg": ""
      ,"data": {
      }
    }
    form = forms.RegistinitForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        checkcode = form.cleaned_data['checkcode']
        newpassword = form.cleaned_data['password']
        repassword = form.cleaned_data['repass']
        vercode = form.cleaned_data['vercode']
        captchakey = form.cleaned_data['captchakey']
        if check_captcha(captchakey, vercode):
            UserResetpsd_get = models.UserResetpsd.objects.filter(email = email,is_start=True,urlarg=checkcode,is_check=False).first()
            if UserResetpsd_get:
                user= UserResetpsd_get.user
                if checkpsd(newpassword):
                    if newpassword and newpassword==repassword:
                        user.set_password(newpassword)
                        user.is_active=True
                        user.save()
                        UserResetpsd_get.is_check=True
                        UserResetpsd_get.save()
                        json_data['code'] = 0
                        json_data['msg']  = '重置成功，请重新登陆'
                    else:
                        json_data['msg']  = '两次密码不一致'
                else:
                    json_data['msg']  = '密码不符合安全规范'
            else:
                json_data['msg']  = '校验信息有误，系统已记录错误信息'
        else:
            json_data['msg'] = '验证码不正确，请重试'
    else:
        json_data['msg'] = '请检查输入'
    return JsonResponse(json_data)
    

@api_view(['GET'])
def getmenu(request):
    user = request.user
    json_data = {
      "code": 0
      ,"msg": ""
      ,"data": {
      }
    }
    role_list= models.Role.objects.none()
    menu_list= models.Menu.objects.none()
    if not user.is_superuser:
        role_list = user.profile.roles.all()
        for role in role_list:
            menu_list = menu_list | role.menu.all()
    else:
        menu_list = models.Menu.objects.filter(parent__isnull=True)
    menu_list = menu_list.order_by('order')
    if not menu_list and not role_list:
        json_data['code']=1
        json_data['msg']='无可访问的资源或菜单初始化失败,请联系管理员'
        json_data['data'] = [{
            "title": "主页"
            ,"icon": "layui-icon-home"
            ,"list": [{
              "title": "控制台"
              ,"jump": "index"
            }]
          }]
    else:
        json_data['data'] = menu.menutotree(menu_list, True)
    return JsonResponse(json_data)
