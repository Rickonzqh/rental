#coding:utf-8
'''
Created on 2019/7/10

@author: rickon
'''
from django.http import JsonResponse
from django.middleware import csrf

def get_token(request):
    json_data = {
      "code": 0
      ,"msg": ""
      ,"data": {}
    }
    token = csrf.get_token(request)
    json_data['data']['token']=token
    return JsonResponse(json_data)

