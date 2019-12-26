#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone
from enum import unique
#from AssetManage import models as assetmodels

# Create your models here.

class Area(models.Model):
    name = models.CharField(verbose_name = '区域名称',max_length = 100)
    parent = models.ForeignKey('self',verbose_name = '上级区域',related_name='area_area',null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        title_list = [self.name]
        p=self.parent
        while p:
            title_list.insert(0,p.name)
            p = p.parent
        return '-'.join(title_list)
    
    class Meta: 
        verbose_name = 'Area' 
        verbose_name_plural = '区域划分' 
    
class Company(models.Model):
    name = models.CharField(verbose_name = '公司名称',max_length = 100)
    key = models.CharField(verbose_name = '机构代码',max_length = 100,unique=True)
    address = models.CharField(verbose_name = '公司地址',max_length = 200)
    web = models.CharField(verbose_name = '官网地址',max_length = 100,null=True,blank=True)
    manage = models.CharField('法定代表人',max_length=50)
    idcard = models.CharField('身份证号',max_length=100)
    mobilephone = models.CharField('手机号码',max_length=50)
    teamname = models.CharField(verbose_name = '团队名称',max_length = 100)
    teamaddress = models.CharField(verbose_name = '团队地址',max_length = 200)
    #parent = models.ForeignKey('self',verbose_name = '上级公司',related_name='company_company',null=True,blank=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User,related_name='company_for_user',verbose_name='所属用户',null=True,blank=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Company' 
        verbose_name_plural = '企业信息'     


class Department(models.Model):
    name = models.CharField(verbose_name = '部门名称',max_length = 100)
    parent = models.ForeignKey('self',verbose_name = '上级部门',related_name='department_depaetment',null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        title_list = [self.name]
        p=self.parent
        while p:
            title_list.insert(0,p.name)
            p = p.parent
        return '-'.join(title_list)
    
    class Meta: 
        verbose_name = 'Department' 
        verbose_name_plural = '部门划分' 
        
        
class Menu(models.Model):
    order = models.IntegerField('排序',default = 0)
    name = models.CharField(verbose_name = '菜单名称',max_length = 100)
    key = models.CharField(verbose_name = '菜单标识',max_length = 50)
    icon = models.CharField(verbose_name = '菜单图标',max_length = 100)
    jump = models.CharField(verbose_name = '跳转地址',max_length = 200,null=True,blank=True)
    parent = models.ForeignKey('self',verbose_name = '上级菜单',related_name='menu_menu',null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        title_list = [self.name]
        p=self.parent
        while p:
            title_list.insert(0,p.name)
            p = p.parent
        return '-'.join(title_list)
    
    class Meta: 
        verbose_name = 'Menu' 
        verbose_name_plural = '菜单管理' 


class Permission(models.Model):
    name = models.CharField(verbose_name = '权限名称',max_length = 100)
    url = models.CharField(verbose_name = '授权地址',max_length=200)
    menu = models.ForeignKey(Menu,verbose_name = '菜单关联',related_name='permission_menu',null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Permission' 
        verbose_name_plural = '权限关联' 
        

class Role(models.Model):
    name = models.CharField('角色名称',max_length=25,unique=True)
    description = models.TextField('角色描述',null=True,blank=True)
    menu = models.ManyToManyField(Menu,verbose_name='角色关联',related_name='role_menu')
    
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Role' 
        verbose_name_plural = '角色管理' 


class UserResetpsd(models.Model):
    email = models.EmailField('邮箱地址')
    urlarg = models.CharField('校验参数',max_length=50)
    is_check = models.BooleanField('是否审批',default=False)
    is_start = models.BooleanField('是否有效',default=False)
    updatetime = models.DateField('更新时间',auto_now=True)
    user = models.ForeignKey(User,verbose_name='申请人',related_name='reseppsd_user',on_delete=models.CASCADE,)
    def __str__(self):
        return self.email
    
    class Meta: 
        verbose_name = 'UserResetpsd' 
        verbose_name_plural = '操作校验' 


        
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_num =  models.CharField('员工编号',max_length=50,null=True,blank=True)
    title =  models.CharField('职位名称',max_length=50,null=True,blank=True)
    
    
    telephone = models.CharField('联系电话',max_length=50,null=True,blank=True)
    mobilephone = models.CharField('手机号码',max_length=50)
    description = models.TextField('用户说明',null=True,blank=True)
    error_count = models.IntegerField('错误登录',default=0)
    login_count = models.IntegerField('登录统计',default=0)
    lock_time = models.DateTimeField('锁定时间',default = timezone.now)
    
    #company = models.ForeignKey(Company,verbose_name='企业信息',related_name='user_company',null=True,blank=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,verbose_name='企业角色',related_name='user_department',null=True,blank=True,on_delete=models.CASCADE)
    parent = models.ManyToManyField(User,verbose_name='汇报对象',blank=True,related_name='user_parent')
    area =  models.ForeignKey(Area,verbose_name='区域关联',related_name='user_area',null=True,on_delete=models.CASCADE,limit_choices_to={'parent__isnull':True})
    
    roles = models.ManyToManyField(Role,verbose_name='管理人员',related_name='user_role')
    
    def __str__(self):
        return self.user.username
    
    class Meta: 
        verbose_name = 'Profile' 
        verbose_name_plural = '用户属性' 
 
@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        Profile.objects.get_or_create(user=instance)  

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
