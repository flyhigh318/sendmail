# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 18:17
# @Author  : Abner
# @File    : ExecMysql.py
# @Software: PyCharm

import MySQLdb
from .DateTime import Date

class Mysql(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.db = kwargs['database']
        self.passwd = kwargs['passwod']
        self.port = kwargs['port']

    def exec_sql(self, sql):
        """
        :param mysql_host: 数据库主机带端口号
        :param mysql_user: 数据库用户
        :param mysql_password: 密码
        :param mysql_schema: 库
        :param sql: mysql_query_str: 查询语句
        """
        conn = MySQLdb.connect(self.host, self.user, self.passwd, self.db, self.port, charset='utf8')
        cursor = conn.cursor()
        count = cursor.execute(sql)
        if count == 0:
            sql = "SELECT '" + Date().get_yesterday().strftime('%Y%m%d') + "没数据' as nodata"
            print(sql)
            count = cursor.execute(sql)
        cursor.scroll(0, mode='absolute')
        results = cursor.fetchall()
        fields = cursor.description
        return [ fields, results ]