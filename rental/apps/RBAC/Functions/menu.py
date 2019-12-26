#coding:utf-8
'''
Created on 2018年11月8日

@author: 残源
'''
from django.utils.html import escape

def menutotree(menu_list,is_root=True):
    menu_tree = []
    for menu_get in menu_list:
        menu_node = {
            'name':escape(menu_get.key)
            ,'title':escape(menu_get.name)
            ,'icon':escape(menu_get.icon)
            ,'list':[]
            }
        if menu_get.menu_menu.all():
            menu_node['list'] = menutotree(menu_get.menu_menu.all(),False)
        if not is_root:
            menu_node['jump'] = escape(menu_get.jump)
        menu_tree.append(menu_node)
    return menu_tree
            
    

