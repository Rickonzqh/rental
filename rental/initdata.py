#coding:utf-8
'''
Created on 2018年11月8日

@author: 残源
'''

import django,os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Framework.settings')
django.setup()
from RBAC.models import Permission,Menu,Department,Role,Area
from django.contrib.auth.models import User

def initmenu():
    menu_list = [
         
         {'name':'商品管理','key':'goodsmanage','icon':"layui-icon-form",'jump':'','parent':''},
         {'name':'商品列表','key':'rootlist','icon':"",'jump':'goodsmanage/goodslist','parent':'goodsmanage'},
         {'name':'收藏列表','key': 'colletclist','icon': "",'jump': 'goodsmanage/collectlist', 'parent': 'goodsmanage'},

         {'name':'苏宁','key':'suning','icon':"layui-icon-form",'jump':'','parent':''},
         {'name':'商品列表','key':'rootlist','icon':"",'jump':'suning/goodslist','parent':'suning'},
         {'name':'收藏列表','key': 'colletclist','icon': "",'jump': 'suning/collectlist', 'parent': 'suning'},

         {'name':'系统设置','key':'set','icon':"layui-icon-set",'jump':'','parent':''},
         {'name':'我的设置','key':'user','icon':"",'jump':'','parent':'set'},
         {'name':'修改密码','key':'password','icon':"",'jump':'set/user/password','parent':'user'},
         {'name':'企业信息','key':'company','icon':"",'jump':'set/user/company','parent':'user'},
         ]
    for item in menu_list:
        menu_get = Menu.objects.get_or_create(
            name=item['name']
            ,key=item['key']
            ,icon=item['icon']
            ,jump=item['jump']
            )
        menu_get = menu_get[0]
        menu_get.parent= Menu.objects.filter(key=item['parent']).first()
        menu_get.save()
    print('initmenu OK')
    
def initPermission():
    #权限对应的菜单均为第一级菜单，情确保访问该菜单相关页面url均已授权至菜单
    permission_list =[
        {'name':'用户管理','url':'/super/','menu':'administrators'},
        
        ]
    for item in permission_list:
        permission_get = Permission.objects.get_or_create(
            name=item['name'],
            url=item['url'],
            )
        permission_get = permission_get[0]
        permission_get.menu = Menu.objects.filter(key=item['menu']).first()
        permission_get.save()
    print('initPermission OK')
    
def initRole():
    role_list=[
        {'name':'普通账号','description':'系统基本使用权限','menu':['goodsmanage','set']},
        {'name':'管理账号','description':'普通管理权限','menu':['administrators']},
        ]
    for item in role_list:
        role_get = Role.objects.get_or_create(name=item['name'])
        role_get=role_get[0]
        role_get.description=item['description']
        for menu_get in Menu.objects.filter(key__in=item['menu']):
            role_get.menu.add(menu_get)
        role_get.save()
    print('initRole ok')

def initArea():
    area_list =[
        {'name':'广东省','parent':''},
        {'name':'惠州市','parent':'广东省'},
        {'name':'广州市','parent':'广东省'},
        {'name':'深圳市','parent':'广东省'},
        {'name':'佛山市','parent':'广东省'},
        {'name':'汕头市','parent':'广东省'},
        {'name':'东莞市','parent':'广东省'},
        ]
    for item in area_list:
        item_get = Area.objects.get_or_create(name=item['name'])
        item_get = item_get[0]
        item_get.parent=Area.objects.filter(name=item['parent']).first()
        item_get.save()
    print('initArea ok')
    
def initDepartment():
    #给超级管理员设置特殊部门
    department_list =[
        {'name':'super','parent':''},
        ]
    for item in department_list:
        Department.objects.get_or_create(
            name=item['name'],
            )
    admin_list = User.objects.filter(is_superuser=True)
    if admin_list:
        for user in admin_list:
            user.profile.department = Department.objects.filter(name = 'super').first()
            user.save()
    else:
        print('请先创建超级管理员账号')
    print('initPermission OK')


if __name__ == "__main__":
    initmenu()
    initPermission()
    initRole()
    initArea()
    initDepartment()
