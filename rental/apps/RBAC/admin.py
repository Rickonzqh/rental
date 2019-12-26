#coding:utf-8
from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Area)
admin.site.register(models.Department)
admin.site.register(models.Menu)
admin.site.register(models.Permission)
admin.site.register(models.Role)
admin.site.register(models.UserResetpsd)
admin.site.register(models.Profile)
admin.site.register(models.Company)