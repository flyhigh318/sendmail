# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 18:55
# @Author  : Abner
# @File    : ttjiekuan_user_plan_text.py
# @Software: PyCharm

from SetBaseDir import *
from config.Mysql import mysql_info
from commom.ExecMysql import Mysql
from commom.FormExcel import Excel
from commom.Sendmail import Mail
from commom.HandleMailConfig import mail_config
from commom.DateTime import Date
from commom.Logger import Logger

if __name__ == '__main__':
    # set logger name
    function_name = 'ttjiekuan_user_html.py'
    logger = Logger(function_name).getLogger()

    try:
        # 近7天放款小计
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

        logger.info("近7天放款小计")
        fields, results = Mysql(**mysql_info).exec_sql(sql)

        # <td align="center"><h4>日期</h4></td>
        # <td align="center"><h4>放款账单量(单)</h4></td>
        # <td align="center"><h4>放款金额(元)</h4></td>
        last_week_detail = ""
        for item in results:
            last_week_detail = last_week_detail + """
              <tr>
                <td>{0}</td>
                <td align="right">{1}</td>
                <td align="right">{2}</td>
              </tr>
            """.format(item[0], item[1], format(item[2], ','))

        # ================================7天/本月 放款统计
        # 2018.06.01 修正bug日期获取跨月的问题
        # 2018.06.11 放到下面的SQL做统计 COUNT(acb.id) AS '平台累计放款账单量(单)',     #             ROUND(SUM(acb.practical_money) / 100, 0) AS '平台累计放款金额(元)'
        sql = """
                SELECT 
                COUNT(IF(acb.loaned_date > DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND acb.loaned_date < CURDATE(), acb.id, NULL)) AS '近7天放款账单量(单)', 
                ROUND(SUM(IF(acb.loaned_date > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND acb.loaned_date < CURDATE(), acb.practical_money, 0))/ 100,0) AS '近7天放款金额(元)',
    
                COUNT(IF(acb.loaned_date >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY) ,'%Y-%m-01') AND acb.loaned_date < DATE_ADD(LAST_DAY(DATE_SUB(CURDATE(), INTERVAL 1 DAY)), INTERVAL 1 DAY)  ,acb.id,NULL )) AS '本月放款账单量(单)', 
                ROUND(SUM(IF(acb.loaned_date >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY) ,'%Y-%m-01') AND acb.loaned_date < DATE_ADD(LAST_DAY(DATE_SUB(CURDATE(), INTERVAL 1 DAY)), INTERVAL 1 DAY),acb.practical_money,0 ))  / 100, 0) AS '本月放款金额(元)'
            FROM
                app_cash_bill acb
                    LEFT JOIN admin_apply aa 
                            ON acb.id = aa.bill_id
            WHERE acb.loaned_date IS NOT NULL
              AND aa.`code` NOT IN ('X_1_20180306171415115','X_1_20180307153538422','X_1_20180308141303214','X_1_20180319141944084','X_1_20180319150349293','X_1_20180323145728376','X_13710_20180517202940834');
        """

        logger.info("7天/本月 放款统计")
        fields, results = Mysql(**mysql_info).exec_sql(sql)
        # get data
        wk_day_cnt = results[0][0]
        wk_day_money_sum = results[0][1]
        mn_day_cnt = results[0][2]
        mn_day_money_sum = results[0][3]
        # al_day_cnt = results[0][4]
        # al_day_money_sum = results[0][5]

        '''
            <td align="center"><h4>近7天放款账单量(单)</h4></td>
            <td align="center"><h4>近7天放款金额(元)</h4></td>
            <td align="center"><h4>本月放款账单量(单)</h4></td>
            <td align="center"><h4>本月放款金额(元)</h4></td>
        '''
        mail_app_cash_bill_summary = """
              <tr>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
                <td align="right">{2}</td>
                <td align="right">{3}</td>
          </tr>
        """.format(wk_day_cnt, format(wk_day_money_sum, ','),
                   mn_day_cnt, format(mn_day_money_sum, ','))

        # ======================当日及累计
        sql = """
            SELECT
                COUNT(IF(DATE_FORMAT(acbi.practical_date,'%Y%m%d') = DATE_SUB(CURDATE(),INTERVAL 1 DAY),acbi.refund_money,NULL)) 
                AS today_refund_count, -- 当日回款账单量(单)
                ROUND(SUM(IF(DATE_FORMAT(acbi.practical_date, '%Y%m%d') = DATE_SUB(CURDATE(), INTERVAL 1 DAY), acbi.refund_money, 0)) / 100, 2)
                AS today_refund_money, -- 每日回款(元)        
                COUNT(IF(DATE_FORMAT(acbi.end_date, '%Y%m%d') = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND acbi.practical_date IS NULL, acbi.id, NULL))
                AS today_overdue_count, -- 每日逾期数量(单)
                ROUND(SUM(IF(DATE_FORMAT(acbi.end_date,'%Y%m%d') = DATE_SUB(CURDATE(),INTERVAL 1 DAY) AND acbi.practical_date IS NULL,acbi.total_money,0)) / 100,2) 
                AS today_overdue_money, -- 每日逾期本息(元)
            
                COUNT(DISTINCT if(acbi.create_date < curdate(), acbi.bill_id, null))
                AS total_principal_order_count, -- 平台累计放款账单量(单)
                ROUND(SUM(IF(acbi.create_date < CURDATE(), acbi.principal_money, 0)) / 100, 0)
                AS total_principal_order_money, -- 平台累计放款金额(元)
                COUNT(DISTINCT IF(acbi.practical_date < CURDATE(), acbi.bill_id, 0)) 
                AS total_refund_order_count, -- 平台累计回款账单量(单)
                ROUND(SUM(IF(acbi.practical_date < CURDATE(), acbi.principal_money, 0)) / 100,0) 
                AS total_refund_principal_money, -- 平台累计回款本金(元)
                ROUND(SUM(IF(acbi.practical_date < CURDATE(), acbi.refund_money, 0)) / 100,0)
                AS total_refund_money, -- 平台累计回款金额(元)
            
                1000000 - ROUND(SUM(IF(acbi.create_date < CURDATE(), acbi.principal_money, 0)) / 100, 2) + ROUND(SUM(IF(acbi.practical_date < CURDATE(), acbi.refund_money, 0)) / 100, 2) 
                AS cash_pool, -- 资金池余额(元)
                ROUND(SUM(IF(acbi.create_date<CURDATE() AND acbi.practical_date IS NULL, acbi.principal_money, 0)) / 100, 2)
                AS principal_money, -- 贷款余额(元)
                
                COUNT(IF(acbi.end_date < curdate() AND acbi.cash_bill_item_status = 1, acbi.id, NULL))
                AS total_overdue_count, -- 累计逾期未还账单量(单)
                ROUND(SUM(IF(acbi.end_date < CURDATE() AND acbi.cash_bill_item_status = 1, acbi.principal_money,0)) / 100,2) 
                AS total_overdue_money -- 累计逾期未还本金(元)
            FROM   app_cash_bill_item acbi LEFT OUTER JOIN admin_apply aa ON acbi.bill_id = aa.bill_id
            WHERE  aa.`code` NOT IN ('X_1_20180306171415115', 'X_1_20180307153538422', 'X_1_20180308141303214', 'X_1_20180319141944084',
                                     'X_1_20180319150349293', 'X_1_20180323145728376', 'X_13710_20180517202940834');
                                     
        """

        logger.info("当日及累计")
        fields, results = Mysql(**mysql_info).exec_sql(sql)

        # get data
        today_refund_count = results[0][0]  # 当日回款账单量(单)
        today_refund_money = results[0][1]  # 每日回款(元)
        today_overdue_count = results[0][2]  # 每日逾期数量(单)
        today_overdue_money = results[0][3]  # 每日逾期本息(元)

        total_principal_order_count = results[0][4]  # 平台累计放款账单量(单)
        total_principal_order_money = results[0][5]  # 平台累计放款金额(元)
        total_refund_order_count = results[0][6]  # 平台累计回款账单量(单)
        total_refund_principal_money = results[0][7]  # 平台累计回款本金(元)
        total_refund_money = results[0][8]  # 平台累计回款金额(元)

        cash_pool = results[0][9]  # 资金池余额(元)
        principal_money = results[0][10]  # 贷款余额(元)

        # get data
        total_overdue_count = results[0][11]  # 累计逾期未还账单量(单)
        total_overdue_money = results[0][12]  # 累计逾期未还本金(元)
        logger.info("分配变量")
        '''
            <td align="center"><h4>当天回款账单量(单)</h4></td>
            <td align="center"><h4>当天回款金额(元)</h4></td>
            <td align="center"><h4>当天逾期账单量(单)</h4></td>
            <td align="center"><h4>当天逾期本息(元)</h4></td>
        '''

        mail_acb_refund_overdue_cash_principal_summary = """
          <tr>
            <td align="right">{0}</td>
            <td align="right">{1}</td>
            <td align="right">{2}</td>
            <td align="right">{3}</td>
          </tr>
        """.format(format(today_refund_count, ','),
                   format(today_refund_money, ','),
                   format(today_overdue_count, ','),
                   format(today_overdue_money, ','), )

        '''
            <td align="center"><h4>平台累计放款账单量(单)</h4></td>
            <td align="center"><h4>平台累计放款金额(元) </h4></td>
            <td align="center"><h4>累计回款账单量(单)</h4></td>
            <td align="center"><h4>累计回款本金(元)</h4></td>
            <td align="center"><h4>累计回款金额(元)</h4></td>
        '''
        mail_acb_total_summary = """
              <tr>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
                <td align="right">{2}</td>
                <td align="right">{3}</td>
                <td align="right">{4}</td>
              </tr>
            """.format(format(total_principal_order_count, ','),
                       format(total_principal_order_money, ','),
                       format(total_refund_order_count, ','),
                       format(total_refund_principal_money, ','),
                       format(total_refund_money, ','),
                       )

        '''
            <td align="center"><h4>累计逾期未还账单量(单)</h4></td>
            <td align="center"><h4>累计逾期未还本金(元)</h4></td>
            <td align="center"><h4>贷款余额(元)</h4></td>
            <td align="center"><h4>资金池余额(元)</h4></td>
        '''

        mail_acb_overdue_principal_cash_summary = """
              <tr>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
                <td align="right">{2}</td>
                <td align="right">{3}</td>
              </tr>        
        """.format(format(total_overdue_count, ','),
                   format(total_overdue_money, ','),
                   format(principal_money, ','),
                   format(cash_pool, ','),
                   )

        logger.info("生成邮件内容")
        '''
           重新设置发送邮件的title， body， 附件的路径，以及附件的文件名，否则会采用默认配置。
        '''

        mail_info = mail_config()
        mail_info['title'] = '【东方星空-天天借款】' + '放款统计' + Date().format_yesterday_cn()
        mail_info['body'] = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>无标题文档a</title>
        </head>
        
        <body>
        
        <p>你们好:</p>
        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;近7天放款统计如下</p>
        <table width="350" border="1">
          <tr>
            <td align="center"><h4>日期</h4></td>
            <td align="center"><h4>放款账单量(单)</h4></td>
            <td align="center"><h4>放款金额(元)</h4></td>
          </tr>
          {0} 
        </table>
        <p>&nbsp;</p>
        <table width="800" border="1" >
          <tr>
            <td align="center"><h4>近7天放款账单量(单)</h4></td>
            <td align="center"><h4>近7天放款金额(元)</h4></td>
            <td align="center"><h4>本月放款账单量(单)</h4></td>
            <td align="center"><h4>本月放款金额(元)</h4></td>
          </tr>
            {1}
        </table>
        <p>&nbsp;</p>
        <table width="800" border="1" >
          <tr>
            <td align="center"><h4>当天回款账单量(单)</h4></td>
            <td align="center"><h4>当天回款金额(元)</h4></td>
            <td align="center"><h4>当天逾期账单量(单)</h4></td>
            <td align="center"><h4>当天逾期本息(元)</h4></td>
          </tr>
            {2}
        </table>
        <p>&nbsp;</p>
        <table width="800" border="1" >
          <tr>
            <td align="center"><h4>平台累计放款账单量(单)</h4></td>
            <td align="center"><h4>平台累计放款金额(元) </h4></td>
            <td align="center"><h4>累计回款账单量(单)</h4></td>
            <td align="center"><h4>累计回款本金(元)</h4></td>
            <td align="center"><h4>累计回款金额(元)</h4></td>
          </tr>
          {3}
        </table>
        <p>&nbsp;</p>
        <table width="800" border="1" >
          <tr>
            <td align="center"><h4>累计逾期未还账单量(单)</h4></td>
            <td align="center"><h4>累计逾期未还本金(元)</h4></td>
            <td align="center"><h4>贷款余额(元)</h4></td>
            <td align="center"><h4>资金池余额(元)</h4></td>
          </tr>
          {4}
        </table>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        </body>
        </html>
        """.format(last_week_detail, mail_app_cash_bill_summary, mail_acb_refund_overdue_cash_principal_summary, mail_acb_total_summary, mail_acb_overdue_principal_cash_summary)
        # print log info
        logger.info("DEBUG info: ===========================")
        logger.info('{0} {1} {2}'.format(mail_info["receivers"], "|||", mail_info["to_str"]))
        logger.info('{0} {1} {2}'.format(mail_info["cc_receivers"], "|||", mail_info["cc_str"]))
        logger.info('{0} {1} {2}'.format(mail_info["cc_secret_receivers"], "|||", mail_info["cc_sec_str"]))
        logger.info(mail_info["title"])
        logger.info(mail_info['body'])
        # send mail
        # Mail(**mail_info).send_html_mail(**mail_info)
        logger.info("Send mail success")
    except Exception as ex:
        logger.error(ex)
