# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 17:47
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Mail.py
# @Software: PyCharm

mail_info = {
    "sender": 'report@test.com',
    "smtpserver": 'smtp.mxhichina.com',
    "username": 'report@test.com',
    "password": 'test',
    # =================prod===========================
    # 配置邮件接收者
    "receivers": [
        'test@test.com',
        'test1@test.com',
    ],
    # 配置邮件抄送者
    "cc_receivers": [
        'test2@test.com',
    ],
    # 密送
    "cc_secret_receivers": [
        'yun_wei_666@163.com',
    ],
    # ================================================
    # #test
    # #配置邮件接收者
    # "receivers": [
    #     'MOLOKO@qq.com',
    # ],
    # # test
    # # 配置邮件抄送者
    # "cc_receivers": [
    #     'yun_wei_666@163.com',
    # ],
    # # test
    # # 密送
    # "cc_secret_receivers": [
    #     'yun_wei_666@163.com',
    # ],
    # 配置发送邮件标题
    "title": '【xxxx-xxxx】',
    # 配置发送邮件正文
    "body": '你们好，附件为xxxx-xxxx-数据，请查收，谢谢.',
    # 配置发送附件路径
    "path": '/tmp',
    # 配置发送附件名称
    "name": 'a.xls',

}
