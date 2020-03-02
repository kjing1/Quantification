# python 3.7.4
# coding = utf-8
# filename ts_base_data.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from db import dbpool
import time
import log
import tus.api as tsapi

logfile = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\logs\\log_base_data-%s.txt'
startdate = '20200201'
enddate = '20200229'

if __name__ == '__main__':
    stocks_list = []
    today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('-------------------%s-------------------' % today)

    # 初始化日志
    logger = log.init_logging(logfile, 'debug')
    # 链接数据库
    conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
    # 初始化tushare
    pro = tsapi.init_tushare(logger, tsapi.MYTOKEN)
    if pro is None:
        print('Init tushare error, exit')
        exit(1)
    # 获取股票ts代码
    for d in conn.getAll('select ts_code from t_stocks'):
        stocks_list.append(d['ts_code'])

    # 获取日行情
    print('%s : Get daily from %s-%s' % (today, startdate, enddate))
    c = tsapi.insert_daliy_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=-1)
    if c >= 0:
        print('%s : All insert %d daily datas' % (today, c))
    else:
        print('%s : Not found data or get some errors' % today)

    # 获取周行情
    print('%s : Get weekly from %s-%s' % (today, startdate, enddate))
    c = tsapi.insert_weekly_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=-1)
    if c >= 0:
        print('%s : All insert %d weekly datas' % (today, c))
    else:
        print('%s : Not found data or get some errors' % today)

    # 获取月行情
    print('%s : Get weekly from %s-%s' % (today, startdate, enddate))
    c = tsapi.insert_weekly_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=-1)
    if c >= 0:
        print('%s : All insert %d weekly datas' % (today, c))
    else:
        print('%s : Not found data or get some errors' % today)

    print('-------------------%s-------------------' % today)
