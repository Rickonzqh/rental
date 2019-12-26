#coding:utf-8

'''
Created on 20196/16

@author: rickon
'''
from rest_framework import serializers
from django.contrib.auth.models import User
from RBAC import models as rbacmodels

class ExterNameField(serializers.CharField):
    def to_representation(self, value):
        return value.username


class roleslistField(serializers.CharField):
    def to_representation(self, value):
        data_list = []
        for row in value:
            data_list.append(row.name)
        return data_list


class parentlistField(serializers.CharField):
    def to_representation(self, value):
        data_list = []
        if value:
            for row in value:
                data_list.append(row.username)
        else:
            pass
        return data_list


class UserManageSerializer(serializers.ModelSerializer):
    # department = serializers.CharField(source = 'profile.department.name')
    mobilephone = serializers.CharField(source = 'profile.mobilephone')
    roles = roleslistField(source="profile.roles.all")
    parent = parentlistField(source="profile.parent.all")

    class Meta:
        model = User
        fields = ('id','username','email','mobilephone','is_active','roles','parent')  


class CompanySerializer(serializers.ModelSerializer):
    user = ExterNameField()
    class Meta:
        model = rbacmodels.Company
        fields = "__all__"
