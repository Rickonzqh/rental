#coding:utf-8
'''
Created on 2019/7/13

@author: rickon
'''

from rest_framework import serializers
from . import models


class ParentIdField(serializers.CharField):
    def to_representation(self, value):
        return value if value else 0


class RootTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = ('id', 'name')


class TypeInfoSerializer(serializers.ModelSerializer):
    parentId = serializers.SerializerMethodField()
    title = serializers.CharField(source='name')

    class Meta:
        model = models.Type
        fields = ('id', 'title', 'parentId')

    def get_parentId(self, obj):
        return obj.parent_id if obj.parent_id else 0

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = ('id', 'name', 'sku', 'type1', 'type2', 'price')


class CollectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Collect
        fields = ('id', 'name', 'sku', 'type1', 'type2', 'price')

