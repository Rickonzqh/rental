#coding:utf-8
'''
Created on 2019/5/15

@author: rickon
'''

from .. import models

def savemessage(data_get):
    '''
        data_get:{
                'id':'',        //业务id
                'title':'',
                'body':'',
                'url':'',
                'user':'',
            }
    '''
    id = data_get.get('id')
    title = data_get.get('title')
    body = data_get.get('body')
    url = data_get.get('url')
    user = data_get.get('user')

    if id is None or int(id) < 1:
        item_get = models.Message.objects.create(
            title=title,
            body=body,
            url=url,
            user=user
        )
    else:
        item_get = models.Message.objects.filter(id=id, user=user).first()
        if item_get:
            item_get.title = title
            item_get.body = body
            item_get.url = url
            item_get.save()
        else:
            return False
    return True

