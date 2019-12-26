#coding:utf-8

from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


def createLog(data):
    '''
    data={
    'type':'',
    'user':'',
    'action':'',
    'status':'',
    }
    '''
    models.Log.objects.create(
        type=data["type"]
        ,user=data["user"]
        ,action=data["action"]
        ,status=data['status']
        )
    return True


@api_view(['GET'])
def Log_list(request):
    user=request.user
    log_list = models.Log.objects.filter(user=user).order_by('-create_time')[:5]
    log_serializer = serializers.LogSerializer(log_list,many=True)
    data = {
      "code": 0
      ,"msg": ""
      ,"data": log_serializer.data
    }
    return Response(data)