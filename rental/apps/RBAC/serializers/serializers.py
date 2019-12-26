#coding:utf-8
'''
Created on 2018年10月29日

@author: 残源
'''
#from django.contrib.auth.models import User
from .. import models
from rest_framework import serializers
from django.contrib.auth.models import User

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = ('name', 'parent')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('name','key','address','manage','idcard','mobilephone','teamname','teamaddress')


        

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = '__all__'
        

class PermissionSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    class Meta:
        model = models.Permission
        fields = '__all__'
        
        
class RoleSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True)
    class Meta:
        model = models.Role
        fields = '__all__'
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
        
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)  
 
        
class ProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    parent = UserSerializer(many=True)
    area = AreaSerializer()
    role = RoleSerializer(many=True)
    
    class Meta:
        model = models.Profile
        fields = '__all__'
        
    
class Permission_url_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ('url',)


        