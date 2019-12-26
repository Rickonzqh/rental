#coding:utf-8
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers,models
from .Funtions import type_func
from Util.xss import xssfilter
from Util.page import MyPageNumberPagination
# Create your views here.

@api_view(['GET'])
def typelist(request):
    data = {
      "code": 200,
      "msg": "",
      "data": []
    }
    typelist = models.Type.objects.filter()
    if typelist:
        serializers_get = serializers.TypeInfoSerializer(instance= typelist,many=True)
        data['msg'] = 'success'
        data['data'] = xssfilter(serializers_get.data)
    else:
        data['code'] = 1
        data['msg'] = '没有数据'
    return Response(data)

@api_view(['GET'])
def goodslist(request, type_id):
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": []
    }
    key = request.GET.get('key')
    if not key:
        key = ''
    typelist = ''
    if type_id != 0:
        type_get = models.Type.objects.filter(id=type_id)
        typelist = type_func.type2type(type_get.first()) | type_get
    if typelist:
        list_get = models.Goods.objects.filter(
            type__in=typelist,
            name__icontains=key
        )
    else:
        list_get = models.Goods.objects.filter(
            name__icontains=key
        )
    if list_get:
        list_count = list_get.count()
        pg = MyPageNumberPagination()
        list_page = pg.paginate_queryset(list_get, request, 'self')
        serializers_get = serializers.GoodsSerializer(instance=list_page, many=True)
        data['msg'] = 'success'
        data['count'] = list_count
        data['data'] = xssfilter(serializers_get.data)
    else:
        data['code'] = 1
        data['msg'] = '没有数据'
    return Response(data)

@api_view(['GET'])
def collect(request, goods_id):
    data = {
        "code": 1,
        "msg": "",
        "data": []
    }
    user = request.user
    goods_get = models.Goods.objects.filter(id=goods_id).first()
    if goods_get:
        collect_get = models.Collect.objects.filter(sku=goods_get.sku)
        if collect_get:
            data['msg'] = '商品已收藏'
        else:
            collect_get = models.Collect.objects.get_or_create(
                name=goods_get.name
                , sku=goods_get.sku
                , type1=goods_get.type1
                , type2=goods_get.type2
                , price=goods_get.price
                , user=user
            )
            data['msg'] = 'success'
            data['code'] = 0
    else:
        data['msg'] = '商品不存在'
    return Response(data)

@api_view(['GET'])
def collectlist(request):
    data = {
        "code": 0,
        "msg": "",
        "count": '',
        "data": []
    }
    key = request.GET.get('key')
    if not key:
        key = ''
    user = request.user

    list_get = models.Collect.objects.filter(user=user, name__icontains=key).order_by('-create_time')
    if list_get:
        list_count = list_get.count()
        pg = MyPageNumberPagination()
        list_page = pg.paginate_queryset(list_get, request, 'self')
        serializers_get = serializers.CollectSerializer(instance=list_page, many=True)
        data['msg'] = 'success'
        data['count'] = list_count
        data['data'] = xssfilter(serializers_get.data)
    else:
        data['msg'] = '没有数据'
        data['code'] = 1
    return Response(data)

@api_view(['GET'])
def collectdelete(request, collect_id):
    data = {
        "code": 1,
        "msg": "",
        "data": []
    }
    user = request.user
    collect_get = models.Collect.objects.filter(id=collect_id,user=user).first()
    if collect_get:
        collect_get.delete()
        data['code'] = 0
        data['msg'] = '删除成功'
    else:
        data['msg'] = '收藏不存在'
    return Response(data)



