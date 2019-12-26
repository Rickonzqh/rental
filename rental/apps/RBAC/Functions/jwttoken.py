#coding:utf-8
'''
Created on 2018年10月29日

@author: 残源
'''

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainSlidingView
from django.utils.six import text_type

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token = text_type(token)
        
        return token

class MyTokenObtainPairView(TokenObtainSlidingView):
    serializer_class = MyTokenObtainPairSerializer