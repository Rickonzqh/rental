#coding:utf-8
'''
Created on 2018年9月14日

@author: 残源
'''

from rest_framework import serializers
from . import models

class LogSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.Log
        fields=('type','action','status','create_time')