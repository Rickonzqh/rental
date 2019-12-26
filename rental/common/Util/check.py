#coding:utf-8
'''
Created on 2019/7/10

@author: rickon
'''
import re

def checkpsd(passwd):
    p = re.match(r'^(?=.*?\d)(?=.*?[a-zA-Z]).{6,}$', passwd)
    if p:
        return True
    else:
        return False


def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def checkurl(url):
    p = re.compile(r'^https?:/{2}\w.+$')
    if p.match(url):
        return True
    else:
        return False


def checkips(str_get):
    list_get = str_get.split(';');
    for i in list_get:
        res = checkip(i)
        if res:
            return True
    return False


def checphone(phonenum):
    p = re.match(r'^1[34589]\d{9}$', phonenum)
    if p:
        return True
    else:
        return False
