#coding:utf-8
'''
Created on 2019/6/16

@author: rickon
'''

from Framework.settings import WEB_URL

from EmailManage.Functions import email_service

url = WEB_URL


def sendmails(email, data):
    '''
    data={'subject':'',
          'text_content',
          'html_content'}
    '''

    data['toaddrs'] = [email]
    return email_service.send_email(data)


def sendresetpsdmail(email, argu):
    data = {'subject': '信息安全评测中心账号通知',
            'text_content': '',
            'html_content': ''}
    data[
        'text_content'] = "您的密码初始化地址如下:   " + url + "/static/web/start/index.html#/user/forget/type=resetpass" + "注册参数为" + argu + "，如未申请该平台账号，请忽略该邮件"
    data['html_content'] = """
    <p>Dear user:</p>
    <p>    您的信息安全评测中心密码初始化地址已创建，<a href='""" + url + "/static/web/start/index.html#/user/forget/type=resetpass" """'>点我</a>完成账号初始化</p>
    <p>    如点击失效，请前往访问以下地址""" + url + "/static/web/start/index.html#/user/forget/type=resetpass"  """</p>
    <p>    本次操作校验信息如下""" + argu + """</p>
    <p>    如非本人操作，忽略该邮件</p>
    <p>    本邮件为内部管理平台系统邮件，请勿回复</p>
    """
    res = sendmails(email, data)
    if res:
        return True
    else:
        return False


def sendregistmail(username, email, argu):
    data = {'subject': '信息安全评测中心账号通知',
            'text_content': '',
            'html_content': ''}
    data[
        'text_content'] = "您的账号初始化地址如下:   " + url + "/static/web/start/index.html#/user/reg" + "校验参数为" + argu + ",如无申请该平台账号，请忽略该邮件"
    data['html_content'] = """
    <p>Dear user:</p>
    <p>    您的信息安全评测中心账号初始化地址已创建，<a href='""" + url + "/static/web/start/index.html#/user/reg" """'>点我</a>完成账号初始化</p>
    <p>    如点击失效，请前往访问以下地址""" + url + "/static/web/start/index.html#/user/reg"  """</p>
    <p>    用户账号为""" + username + """</p>
    <p>    本次操作校验信息如下""" + argu + """</p>
    <p>    如非本人操作，忽略该邮件</p>
    <p>    本邮件为内部管理平台系统邮件，请勿回复</p>
    """
    res = sendmails(email, data)
    if res:
        return True
    else:
        return False
