#coding:utf-8
from io import BytesIO
from django.shortcuts import HttpResponse

from Captcha.generate import generate_captcha
# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
import datetime
from . import models

@api_view(['GET'])
@permission_classes((AllowAny,))
def create_captcha(request, key):
    stream = BytesIO()
    img, code = generate_captcha()
    img.save(stream, 'PNG')
    models.CaptchaCode.objects.create(code=code.upper(), key=key)
    return HttpResponse(stream.getvalue())

def check_captcha(key, code):
    ### 五分钟有效
    valid_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    #valid_time_out = datetime.datetime.now() - datetime.timedelta(minutes=10)
    captcha = models.CaptchaCode.objects.filter(key=key, code=code.upper(), create_time__gt=valid_time)
    models.CaptchaCode.objects.filter(create_time__lt=valid_time).delete()
    if len(captcha)>0:
        captcha.delete()
        return True
    else:
        captcha.delete()
        return False