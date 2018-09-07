# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 10:58
# @Author  : Abner
# @File    : HandleMailConfig.py
# @Software: PyCharm

from config.Mail import mail_info

# 把mail_info["receivers"]与mail_info["cc_receivers"]的列表转成str形式

def mail_config():

    mail_info['to_str'] = ','.join(mail_info['receivers'])
    mail_info['cc_str'] = ','.join(mail_info['cc_receivers'])
    mail_info['cc_sec_str'] = ','.join(mail_info['cc_secret_receivers'])
    return mail_info
