# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 21:39
# @Author  : Abner
# @File    : DateTime.py
# @Software: PyCharm

import datetime

class Date(object):

    def __init__(self):
        pass

    def get_yesterday(self):
        """
        获取昨天日期
        :return: date昨天日期
        """
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday

    def format_yesterday_cn(self):
        str_yesterday = self.get_yesterday()
        str_yesterday_year = str_yesterday.strftime('%Y')
        str_yesterday_month = str_yesterday.strftime('%m')
        str_yesterday_day = str_yesterday.strftime('%d')
        str_yesterday_with_cn = "{0}年{1}月{2}日".format(str_yesterday_year, str_yesterday_month, str_yesterday_day)
        return str_yesterday_with_cn