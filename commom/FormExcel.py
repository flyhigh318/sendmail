# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 18:40
# @Author  : Abner
# @File    : FormExcel.py
# @Software: PyCharm

import xlwt

class Excel(object):

    '''
      fields mysql 数据库 table 表 的 字段,
      results 为 执行 sql语句返回查询列表.
    '''

    def __init__(self, **kwargs):
        self.fields = kwargs['fields']
        self.results = kwargs['results']


    '''
       sheet_name 为 创建的excel sheet 名称,
       out_path 为 输出路径
    '''

    def get_excel(self, **kwargs):
        try:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet(kwargs['sheet_name'], cell_overwrite_ok=True)
            for field in range(0, len(self.fields)):
                sheet.write(0, field, self.fields[field][0])
            row = 1
            col = 0
            for row in range(1, len(self.results) + 1):
                for col in range(0, len(self.fields)):
                    sheet.write(row, col, u'%s' % self.results[row - 1][col])
            workbook.save(kwargs["out_path"])
            return kwargs["out_path"]
        except Exception as e:
            print(e)