#coding:utf-8
'''
Created on 2019/5/1

@author: rickon
'''

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage



from email import (
    charset as Charset, encoders as Encoders, generator, message_from_string,
)
from io import BytesIO, StringIO
import base64

from ..models import EmailAccess,EmailLog


def get_emailaccess():
    emailaccess = EmailAccess.objects.filter(status=True).order_by('update_time').last()
    if emailaccess is None:
        raise RuntimeError("没有启用的邮箱账户信息")

    emailaccess.emailaddr = str(base64.b64decode(emailaccess.emailaddr), 'utf-8')[4:-4]
    emailaccess.password = str(base64.b64decode(emailaccess.password), 'utf-8')[4:-4]
    return emailaccess


def send_email(data):
    '''
    data={
        'toaddrs':'', #list
        'subject':'',
        'text_content':'',
        'html_content':'',
        'attachments':'',#list
    }
    '''
    log = {
        'type': '邮件发送',
        'toaddrs': '',
        'subject': '',
        'content': '',
        'attachments': '',
        'status': False,
        'msg': '',
    }
    try:
        log['toaddrs'] = ';'.join(data.get('toaddrs'))
        log['subject'] = data.get('subject')

        email = get_emailaccess()
        subject = email.subject_prefix + data.get('subject')
        mimePart = MIMEMultipart('mixed')
        mimePart['Subject'] = subject
        mimePart['From'] = Header("{0}<{1}>".format(email.emailaddr, email.emailaddr))  # 发送者
        mimePart['To'] = Header(';'.join(data.get('toaddrs')))  # 接收者

        if data.get('text_content'):
            log['content'] = '#'.join((log['content'],data.get('text_content')))
            text_plain = MIMEText(data.get('text_content'), 'plain', 'utf-8')
            mimePart.attach(text_plain)
        if data.get('html_content'):
            log['content'] = '#'.join((log['content'], data.get('html_content')))
            html_plain = MIMEText(data.get('html_content'), 'html', 'utf-8')
            mimePart.attach(html_plain)
        if data.get('attachments'):
            attachmentstr = ';'.join(data.get('attachments'))
            attachmentstr = attachmentstr.replace('\\', '/')
            data['attachments'] = attachmentstr.split(';')
            log['attachments'] = ';'.join(data.get('attachments'))

            ### 添加附件
            for file in data.get('attachments'):
                fileApart = MIMEApplication(open(file, 'rb').read(), file.split('.')[-1])
                fileApart.add_header('Content-Disposition', 'attachment', filename=file.split('/')[-1])
                mimePart.attach(fileApart)
        server = None
        if email.is_ssl:
            server = smtplib.SMTP_SSL(email.host, email.port)
            server.ehlo()
        else:
            server = smtplib.SMTP(email.host, email.port)
            if email.use_tls:
                server.ehlo()
                server.starttls()
        server.login(email.emailaddr, email.password)
        ret = server.sendmail(email.emailaddr, data.get('toaddrs'), mimePart.as_string())
        server.quit()
        log['status'] = True
        createmailLog(log)
        return True
    except Exception as e:
        log['msg'] = str(e)
    createmailLog(log)
    return False

def createmailLog(data):
    '''
    data={
        'toaddrs':'',
        'subject':'',
        'content':'',
        'attachments':'',
    }
    '''
    EmailLog.objects.create(
        type=data["type"]
        ,toaddrs=data["toaddrs"]
        ,subject=data['subject']
        ,content=data["content"]
        ,attachments=data['attachments']
        ,status=data["status"]
        ,msg=data['msg']
        )
    return True

