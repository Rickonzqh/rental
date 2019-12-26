#coding:utf-8
'''
Created on 2018年11月13日

@author: 残源
'''


def departmentselecttotree(department_list,is_show=True):
    department_tree=[]
    for item  in department_list:
        department_node = {
            'id':item.id
            ,'name':item.name
            ,'open':is_show
            ,'children':[]
            }
        if item.department_depaetment.all():
            department_node['children']=departmentselecttotree(item.department_depaetment.all(),is_show)
        else:
            pass
        department_tree.append(department_node)
    return department_tree


def areaselecttotree(area_list,is_show=True):
    area_tree=[]
    for item  in area_list:
        area_node = {
            'id':item.id
            ,'name':item.name
            ,'open':is_show
            ,'children':[]
            }
        if item.area_area.all():
            area_node['children']=areaselecttotree(item.area_area.all(),is_show)
        else:
            pass
        area_tree.append(area_node)
    return area_tree