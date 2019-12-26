#coding:utf-8
'''
Created on 2019/5/15

@author: rickon
'''

from rest_framework import serializers
from . import models

class ExterNameField(serializers.CharField):
    def to_representation(self, value):
        return value.name

class NoticeListSerializer(serializers.ModelSerializer):
    status = ExterNameField()
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.Notice
        fields = ('id', 'title', 'status', 'time')


class NoticeDetailSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.Notice
        fields = ('id','title','body','status','time')


class MessageListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.Message
        fields = ('id', 'title', 'url','status','time')


class MessageDetailSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.Message
        fields = ('id', 'title', 'body', 'url', 'status', 'time')

