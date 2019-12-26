#coding:utf-8
'''
Created on 2018年12月7日

@author: 残源
'''

from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.authentication import  JWTAuthentication

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

def get_user_jwt(request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = SimpleLazyObject(lambda: get_user_jwt(request))