# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 15:49
# @Author  : Abner
# @File    : send_mail_main.py
# @Software: PyCharm
# 脚本执行主程序

import pexpect
import os,time

class expect(object):

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.cmd = kwargs['cmd']

    def process(self):
        try:
            os.chdir(self.path)
            process = pexpect.spawn(self.cmd[0])
            for command in self.cmd:
                if command == self.cmd[0]:
                    pass
                else:
                    time.sleep(1)
                    process.expect('#')
                    process.sendline(command)
                    time.sleep(2)
            print('邮件已经发送成功，请确认')
            process.sendline('exit')
            process.expect('#')
            process.sendline('exit')
            process.expect(pexpect.EOF)
        except Exception as e:
            print(e)


if __name__ == '__main__':

    project = {

         'path': '/home/devops/ttjiekuan-sendmail-loanbill',
         'cmd' : [ 'pipenv shell',
                   'pip install -r requirements.txt',
                   'cd bin',
                   'python ttjiekuan_user_html.py'
                 ]
    }

    expect(**project).process()

