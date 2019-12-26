from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import AllowAny
from Util.page import MyPageNumberPagination
from rest_framework.decorators import api_view,permission_classes
from Util.xss import xssfilter
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q

from . import models
from . import serializers
from . import forms


@api_view(['GET'])
def noticelist(request):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    user =request.user
    key = request.GET.get('key')
    list_get = ''
    if not key:
        key=''
    if user.is_superuser:
        list_get = models.Notice.objects.filter(
                                            Q(title__icontains = key)
                                           ).order_by('-time')
        list_count = list_get.count()
        pg = MyPageNumberPagination()
        list_page = pg.paginate_queryset(list_get, request, 'self')
        serializers_get = serializers.NoticeListSerializer(instance=list_page, many=True)
        data['msg'] = 'success'
        data['count'] = list_count
        data['data'] = xssfilter(serializers_get.data)
    else:
        data['code'] = 1
        data['msg'] = '没有权限'

    return Response(data)


@api_view(['GET'])
def messagelist(request):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    user =request.user
    key = request.GET.get('key')
    list_get = ''
    if not key:
        key=''

    list_get = models.Message.objects.filter(Q(user=user) &
                                             Q(title__icontains=key)
                                            ).order_by('-time')
    list_count = list_get.count()
    pg = MyPageNumberPagination()
    list_page = pg.paginate_queryset(list_get, request,'self')
    serializers_get = serializers.MessageListSerializer(instance= list_page,many=True)
    data['msg'] = 'success'
    data['count'] = list_count
    data['data'] = xssfilter(serializers_get.data)
    return Response(data)


@api_view(['GET'])
def unreadmessagelist(request):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    user =request.user

    list_get = models.Message.objects.filter(user=user,status=False ).order_by('-time')
    list_count = list_get.count()
    pg = MyPageNumberPagination()
    list_page = pg.paginate_queryset(list_get, request,'self')
    serializers_get = serializers.MessageListSerializer(instance= list_page,many=True)
    data['msg'] = 'success'
    data['count'] = list_count
    data['data'] = xssfilter(serializers_get.data)
    return Response(data)

@api_view(['GET'])
def readallmessage(request):
    data = {
        "code": 0,
        "msg": "",
        "data": {
        }
    }
    user = request.user
    list_get = models.Message.objects.filter(user=user,status=False)
    for item in list_get:
        item.status=True
        item.save()
    return Response(data)

@api_view(['GET'])
def getnotice(request, noticeid):
    user = request.user
    data = {
      "code": 1,
      "msg": "",
      "data": []
    }
    data_get = ''
    if user.is_superuser:
        data_get = models.Notice.objects.filter(id=noticeid).first()
        if data_get:
            serializers_get = serializers.NoticeDetailSerializer(instance=data_get)
            data['msg'] = 'success'
            data['data'] = xssfilter(serializers_get.data)
            data['code'] = 0
    else:
        data['msg'] = '没有权限'
    return Response(data)

@api_view(['GET'])
def getmessage(request, messageid):
    user = request.user
    data = {
      "code": 1,
      "msg": "",
      "data": []
    }
    data_get = ''
    if user.is_superuser:
        data_get = models.Message.objects.filter(id=messageid).first()
        if data_get:
            serializers_get = serializers.MessageDetailSerializer(instance=data_get)
            data['msg'] = 'success'
            data['data'] = xssfilter(serializers_get.data)
            data['code'] = 0
            if data_get.status is False:
                data_get.status = True
                data_get.save()
    else:
        data['msg'] = '没有权限'
    return Response(data)


@api_view(['POST'])
def savenotice(request):
    user = request.user
    data = {
        "code": 1,
        "msg": "",
        "data": {
        }
    }
    log = {
        'type': '通告操作',
        'user': user,
        'action': '保存',
        'status': False,
    }
    if user.is_superuser:
        form = forms.Noticeform(request.POST)
        if form.is_valid():
            id = form.data.get('id')
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']

            item_get = ''
            if id is None or int(id) < 1:
                status_get = models.STATUS.objects.filter(name='草稿').first()
                item_get = models.Notice.objects.create(
                    title=title,
                    body=body,
                    status=status_get,
                    user=user,
                )
                data['code'] = 0
            else:
                item_get = models.Notice.objects.filter(id=id).first()
                item_get.title=title
                item_get.body=body
                item_get.save()
        else:
            data['msg'] = '参数错误'
    else:
        data['msg'] = '没有权限'
    return Response(data)

@api_view(['GET'])
def noticeaudit(request, noticeid, action):
    user = request.user
    data = {
        "code": 1,
        "msg": "",
        "count": '',
        "data": []
    }
    res = False
    if user.is_superuser:

        status_old = None
        if action == 'release':
            status_old = models.STATUS.objects.filter(name='草稿').first()
        elif action == 'sendback':
            status_old = models.STATUS.objects.filter(name='发布').first()
        else:
            data['msg'] = '参数错误'
        if status_old:
            notice_get = models.Notice.objects.filter(id=noticeid, status_id=status_old.id).first()
            if notice_get:
                if action == 'release':
                    try:
                        status_get = models.STATUS.objects.filter(name='发布').first()
                        notice_get.status = status_get
                        notice_get.save()
                        user_list = User.objects.filter()
                        for user_item in user_list:
                            item_get = models.Message.objects.create(
                                title=notice_get.title,
                                body=notice_get.body,
                                notice=notice_get,
                                user=user_item,
                            )
                        res = True
                    except:
                        res = False
                elif action == 'sendback':
                    try:
                        status_get = models.STATUS.objects.filter(name='草稿').first()
                        notice_get.status = status_get
                        notice_get.save()
                        models.Message.objects.filter(notice_id=notice_get.id).delete()
                        res = True
                    except:
                        res = False
                else:
                    data['msg'] = '参数错误'

                if res:
                    data['code'] = 0
                    data['msg'] = '操作成功'
                else:
                    data['msg'] = '操作失败，请刷新重试'
            else:
                data['msg'] = '未找到数据，请刷新重试'
    else:
        data['msg'] = '权限错误'
    return Response(data)

@api_view(['GET'])
def noticedelete(request, noticeid):
    user = request.user
    data = {
        "code": 1,
        "msg": "",
        "count": '',
        "data": []
    }
    notice_get =''
    if user.is_superuser:
        notice_get = models.Notice.objects.filter(id=noticeid).first()
        if notice_get:
            notice_get.delete()
            data['code'] = 0
            data['msg'] = '操作成功'
    else:
        data['msg'] = '权限错误'
    return Response(data)

@api_view(['GET'])
def messagedelete(request, messageid):
    user = request.user
    data = {
        "code": 1,
        "msg": "",
        "count": '',
        "data": []
    }
    notice_get =''
    if user.is_superuser:
        notice_get = models.Message.objects.filter(id=messageid).first()
        if notice_get:
            notice_get.delete()
            data['code'] = 0
            data['msg'] = '操作成功'
    else:
        data['msg'] = '权限错误'
    return Response(data)