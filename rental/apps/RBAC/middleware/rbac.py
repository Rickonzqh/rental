#coding:utf-8

'''
Created on 2018年12月7日

@author: 残源
'''


from django.http import JsonResponse
import re
from .. import models

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
    
    
    
def get_permission_url(user):
    role_list = user.profile.roles.all()
    menu_list= models.Menu.objects.none()
    for role in role_list:
        menu_list = menu_list | role.menu.all()
    permission_get = models.Permission.objects.filter(menu__in=menu_list)
    return permission_get
        
        
        
def get_all_permission_url():
    permission_all=''
    menu_list= models.Menu.objects.filter(parent__isnull=True)
    permission_get = models.Permission.objects.filter(menu__in=menu_list)
    for item in permission_get:
        if permission_all !='':
            permission_all += '|'
        permission_all=permission_all + item.url
    permission_all = '^(' + permission_all + ')'
    return permission_all
    
class RbacMiddleware(MiddlewareMixin):
    """
    检查用户的url请求是否是其权限范围内
    """
    def process_request(self, request):
        request_url = request.path_info
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                return None
            else:
                permission_all = get_all_permission_url()
                res_match =re.match(permission_all, request_url)
                if res_match:
                    if request_url.startswith(res_match.group()):
                        permission_list = get_permission_url(user)
                        permission_get = permission_list.filter(url=res_match.group())
                        if permission_get:
                            return None
                        else:
                            return  JsonResponse({'code':1,'msg':'无权访问'})
                    else:
                        return  JsonResponse({'code':1,'msg':'无权访问'})
                else:
                    return None
        return None
        
        
        
        