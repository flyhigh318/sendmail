# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 18:55
# @Author  : Abner.F
# @File    : ttjiekuan_user_plan_text.py
# @Software: PyCharm

from SetBaseDir import *
from config.Mysql import mysql_info
from commom.ExecMysql import Mysql
from commom.FormExcel import Excel
from commom.Sendmail import Mail
from commom.HandleMailConfig import mail_config
from commom.DateTime import Date


if __name__ == '__main__':

    # ================================放款统计
    sql = 'SELECT '\
            'COUNT(IF(acb.loaned_date > DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND acb.loaned_date < CURDATE(), acb.id, NULL)) AS 7day_cnt, ' \
            'ROUND(SUM(IF(acb.loaned_date > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND acb.loaned_date < CURDATE(), acb.practical_money, 0))/ 100,0) AS 7day_money_sum,' \
            'COUNT(acb.id) AS 30day_cnt, ' \
            'ROUND(SUM(acb.practical_money) / 100, 0) AS 30day_money_sum, ' \
            'CURDATE() as td_day, ' \
            'DATE_SUB(CURDATE(), INTERVAL 1 DAY) as yd_day, ' \
            'DATE_SUB(CURDATE(), INTERVAL 7 DAY) as wk_day, ' \
            'DATE_SUB(CURDATE(), INTERVAL 30 DAY) as mn_day ' \
          'FROM app_cash_bill acb '\
        'WHERE acb.loaned_date > DATE_SUB(CURDATE(), INTERVAL 30 DAY)' \
        '    AND acb.loaned_date < CURDATE();'

    fields, results = Mysql(**mysql_info).exec_sql(sql)
    # get data
    wk_day_cnt = results[0][0]
    wk_day_money_sum = results[0][1]
    mn_day_cnt = results[0][2]
    mn_day_money_sum = results[0][3]
    td_day = results[0][4]
    yd_day = results[0][5]
    wk_day = results[0][6]
    mn_day = results[0][7]
    # print(sql)
    # print(wk_day_cnt, wk_day_money_sum, mn_day_cnt, mn_day_money_sum)
    # print(td_day)
    # print(wk_day)
    # print(mn_day)

    sql = """
            SELECT
            dd.`cdate`, IFNULL(b.bill_cnt, 0) bill_cnt, IFNULL(b.money_sum, 0) money_sum
        FROM
            t_dm_date dd
            LEFT JOIN
                (SELECT
                    DATE_FORMAT(b.loaned_date, '%Y-%m-%d') mdate, COUNT(1) bill_cnt, ROUND(SUM(b.`practical_money`) / 100) money_sum
                FROM
                    app_cash_bill b
                WHERE b.loaned_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                    AND b.loaned_date < CURDATE()
                GROUP BY 1) b
                ON b.mdate = dd.`cdate`
        WHERE dd.`cdate` >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            AND dd.`cdate` < CURDATE()
    """

    fields, results = Mysql(**mysql_info).exec_sql(sql)

    last_week_detail = "        日期    放款账单量(单)     放款金额(元)\n"
    for item in results:
        last_week_detail = last_week_detail + "{0}{1}{2}\n".format(item[0].rjust(15), str(item[1]).rjust(12), format(item[2], ',').rjust(20))
        #print("{0}{1}{2}\n".format(item[0], str(item[1]).rjust(8), format(item[2], ',').rjust(10)))

    print(last_week_detail)
    #format(1234567890, ',')
    '''
       重新设置发送邮件的title， body， 附件的路径，以及附件的文件名，否则会采用默认配置。
    '''

    mail_info = mail_config()
    mail_info['title'] = '【东方星空-天天借款】'+ '放款统计' + Date().format_yesterday_cn()
    mail_info['body'] = """
    你们好:
    
        近7天放款统计如下
        
    """ + last_week_detail + \
    """
        
        近7天放款账单量(单)  近7天放款金额(元)  近30天放款账单量(单)  近30天放款金额(元)     
    """ + str(wk_day_cnt).rjust(20)  +  format(wk_day_money_sum, ',').rjust(20)+  str(mn_day_cnt).rjust(30)  + format(mn_day_money_sum, ',').rjust(30) + \
    """
    
    备注：
       1、近7天指{0}到{1}
       2、近30天指{2}到{1}
    """.format(wk_day,yd_day, mn_day)

    print(mail_info)
    Mail(**mail_info).send_mail_without_attach(**mail_info)

