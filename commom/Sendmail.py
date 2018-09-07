# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 17:24
# @Author  : Abner
# @File    : sendmail.py
# @Software: PyCharm

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail(object):

    def __init__(self, **kwargs):
        self.sender = kwargs['sender']
        self.smtpserver = kwargs['smtpserver']
        self.username = kwargs['username']
        self.password = kwargs['password']

    def send_mail_with_attach(self, **kwargs):
         """
         发邮件
         :receviers: 接收人
         :cc_receviers : 抄送
         :param att1_file_path: 附件文件路径
         :param att1_file_name: 附件名
         title 邮件标题
         body 邮件正文
         :return: none
         """
         receiver = kwargs['to_str']
         cc_receiver = kwargs['cc_str']

         # 创建一个带附件的实例
         message = MIMEMultipart()
         message['From'] = self.sender
         message['To'] = receiver
         message['Cc'] = cc_receiver
         message['Subject'] = Header(kwargs['title'], 'utf-8')

         # 邮件正文内容
         message.attach(MIMEText(kwargs['body'], 'plain', 'utf-8'))
         # 构造附件（附件为TXT格式的文本）
         fnames = []

         # 邮件附件名列表
         list_mail_file_name = kwargs['list_file_name']
         # 邮件附件路径列表
         list_mail_file_path = kwargs['list_file_path']

         for item in list_mail_file_path:
             list_index = list_mail_file_path.index(item)

             att_file_path = item
             att_file_name = list_mail_file_name[list_index]
             # att_file_path = kwargs['path']
             # att_file_name = kwargs['name']
             #att = MIMEText(open(att_file_path + "/" + att_file_name, 'rb').read(), 'base64', 'utf-8')
             att = MIMEText(open(att_file_path , 'rb').read(), 'base64', 'utf-8')

             att["Content-Type"] = 'application/octet-stream'
             att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', att_file_name))
             message.attach(att)
             print('添加附件路径:' + att_file_path + ' 文件名:' + att_file_name)

         smtpObj = smtplib.SMTP_SSL()
         smtpObj.connect(self.smtpserver)
         smtpObj.login(self.username, self.password)
         smtpObj.sendmail(self.sender, receiver.split(',') + cc_receiver.split(','), message.as_string())
         print("邮件发送成功！！！")
         smtpObj.quit()

    def send_mail_without_attach(self, **kwargs):
         """
         发邮件--不带附件
         :receviers: 接收人
         :cc_receviers : 抄送
         title 邮件标题
         body 邮件正文
         :return: none
         """
         receiver = kwargs['to_str']
         cc_receiver = kwargs['cc_str']

         # 创建一个带附件的实例
         message = MIMEMultipart()
         message['From'] = self.sender
         message['To'] = receiver
         message['Cc'] = cc_receiver
         message['Subject'] = Header(kwargs['title'], 'utf-8')

         # 邮件正文内容
         message.attach(MIMEText(kwargs['body'], 'plain', 'utf-8'))
         # 构造附件（附件为TXT格式的文本）
         fnames = []

         smtpObj = smtplib.SMTP_SSL()
         smtpObj.connect(self.smtpserver)
         smtpObj.login(self.username, self.password)
         smtpObj.sendmail(self.sender, receiver.split(',') + cc_receiver.split(','), message.as_string())
         print("邮件发送成功！！！")
         smtpObj.quit()

    def send_html_mail(self, **kwargs):
         """
         发HTML格式邮件
         :receviers: 接收人
         :cc_receviers : 抄送
         title 邮件标题
         body 邮件正文
         :return: none
         """
         receiver = kwargs['to_str']
         cc_receiver = kwargs['cc_str']
         cc_sec_receiver = kwargs['cc_sec_str']

         # 创建一个带附件的实例
         message = MIMEMultipart()
         message['From'] = self.sender
         message['To'] = receiver
         message['Cc'] = cc_receiver
         message['Subject'] = Header(kwargs['title'], 'utf-8')

         # 邮件正文内容
         message.attach(MIMEText(kwargs['body'], 'html', 'utf-8'))

         # 构造附件（附件为TXT格式的文本）
         fnames = []

         smtpObj = smtplib.SMTP_SSL()
         smtpObj.connect(self.smtpserver)
         smtpObj.login(self.username, self.password)
         smtpObj.sendmail(self.sender, receiver.split(',') + cc_receiver.split(',') + cc_sec_receiver.split(',') , message.as_string())
         print("HTML邮件发送成功！！！")
         smtpObj.quit()