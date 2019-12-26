#coding:utf-8
'''
Created on 2019/6/16

@author: rickon
'''
from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    #return HttpResponseRedirect('/static/web/start/index.html')
    return render(request, "web/start/index.html")











        
        


 