#coding:utf-8
'''
Created on 2018年11月1日

@author: 残源
'''
from .. import models


def department_child_list(department_id,is_first=True):
    department = models.Department.objects.filter(id =department_id).first()
    if is_first:
        department_lists = []
    else:
        department_lists = [department]
    if department:
        if department.department_depaetment.all():
            department_list = department.department_depaetment.all()
            for department_get  in department_list:
                department_lists.append(department_get)
            department_lists = department_lists +department_child_list(department_get.id,False)
        else:
            pass
    else:
        return []
    return department_lists
        
            

def departmentintree(user):
    department_user =  user.profile.department
    department_list = department_user.department_depaetment.all()
    department_tree=[]
    for department_get  in department_list:
        department_node = {
            'id':department_get.id
            ,'label':department_get.name
            ,'is_department':True
            }
        department_tree.append(department_node)
    return department_tree

        
        
        
        
        
        
