# python 3.7.4
# coding = utf-8
# filename tsdata.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

import tushare as ts
import dbpool
import time
from utils import logto

token = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'
logfile = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\log.txt'
startdate = '20100101'
enddate = '20200131'

if __name__ == '__main__':
    stocks_list = []

    # 链接数据库
    conn = dbpool.MyPymysqlPool('MysqlDatabaseInfo')

    # 初始化tushare
    ts.set_token(token)
    pro = ts.pro_api()

    # 获取所有股票信息并入库
    logto(logfile, 'Get all stocks base information')
    df = pro.stock_basic(exchange='', list_status='', fields='ts_code,symbol,name,area,industry,list_date,fullname,'
                                                             'enname,market,exchange,curr_type,list_status,'
                                                             'delist_date,is_hs')
    for key, val in df.iterrows():
        sql = 'INSERT INTO t_stocks (ts_code, code, name, area, industry, fullname, enname, market, exchange, ' \
              'curr_type, status, date, de_date, is_hs) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", ' \
              '"%s", "%s", "%s", "%s", "%s")' % (val['ts_code'],
                                                 val['symbol'],
                                                 val['name'],
                                                 val['area'],
                                                 val['industry'],
                                                 val['fullname'],
                                                 val['enname'],
                                                 val['market'],
                                                 val['exchange'],
                                                 val['curr_type'],
                                                 val['list_status'],
                                                 val['list_date'],
                                                 val['delist_date'],
                                                 val['is_hs'])
        if conn.insert(sql) == 1:
            print('STOCK_BASIC record: %d-%s, insert successful' % (key, val['ts_code']))
        else:
            print('STOCK_BASIC record: %d-%s, insert failure' % (key, val['ts_code']))
            logto(logfile, 'STOCK_BASIC record: %d-%s, insert failure. SQL: %s' % (key, val['ts_code'], sql))
        stocks_list.append(val['ts_code'])

    logto(logfile, 'All %d stocks.' % len(stocks_list))
    logto(logfile, 'Get all stocks daily quotations, from %s to %s' % (startdate, enddate))
    # 获取所有股票近三年的日行情
    for stock in stocks_list:
        while True:
            try:
                df = pro.daily(ts_code=stock, start_date=startdate, end_date=enddate)
            except Exception as e:
                print('pro.daily: %s' % e)
                logto(logfile, '%s->pro.daily: %s' % (stock, e))
                continue
            else:
                for key, val in df.iterrows():
                    sql = 'INSERT INTO t_daily (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                          'pct_chg, vol, ' \
                          'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                              val['ts_code'],
                              val['trade_date'],
                              val['open'],
                              val['high'],
                              val['low'],
                              val['close'],
                              val['pre_close'],
                              val['change'],
                              val['pct_chg'],
                              val['vol'],
                              val['amount'])
                    if conn.insert(sql) == 1:
                        print('DAILY record: %d-%s, insert successful' % (key, val['ts_code']))
                    else:
                        print('DAILY record: %d-%s, insert failure' % (key, val['ts_code']))
                        logto(logfile, 'DAILY record: %d-%s, insert failure. SQL: %s' % (key, val['ts_code'], sql))
                    conn.end(option='commit')
                break
        time.sleep(1.5)

    # 获取所有股票近三年的周行情
    logto(logfile, 'Get all stocks weekly quotations, from %s to %s' % (startdate, enddate))
    for stock in stocks_list:
        while True:
            try:
                df = pro.weekly(ts_code=stock, start_date=startdate, end_date=enddate,
                                fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except Exception as e:
                print('pro.weekly: %s' % e)
                logto(logfile, '%s->pro.weekly: %s' % (stock, e))
                continue
            else:
                for key, val in df.iterrows():
                    sql = 'INSERT INTO t_weekly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                          'pct_chg, vol, ' \
                          'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                              val['ts_code'],
                              val['trade_date'],
                              val['open'],
                              val['high'],
                              val['low'],
                              val['close'],
                              val['pre_close'],
                              val['change'],
                              val['pct_chg'],
                              val['vol'],
                              val['amount'])
                    if conn.insert(sql) == 1:
                        print('WEEKLY record: %d-%s, insert successful' % (key, val['ts_code']))
                    else:
                        print('WEEKLY record: %d-%s, insert failure' % (key, val['ts_code']))
                        logto(logfile, 'WEEKLY record: %d-%s, insert failure. SQL: %s' % (key, val['ts_code'], sql))
                    conn.end(option='commit')
                break
        time.sleep(1.5)

    # 获取所有股票近三年的月行情
    logto(logfile, 'Get all stocks monthly quotations, from %s to %s' % (startdate, enddate))
    for stock in stocks_list:
        while True:
            try:
                df = pro.monthly(ts_code=stock, start_date=startdate, end_date=enddate,
                                 fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except Exception as e:
                print('pro.monthly: %s' % e)
                logto(logfile, '%s->pro.monthly: %s' % (stock, e))
                continue
            else:
                for key, val in df.iterrows():
                    sql = 'INSERT INTO t_monthly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                          'pct_chg, vol, ' \
                          'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                              val['ts_code'],
                              val['trade_date'],
                              val['open'],
                              val['high'],
                              val['low'],
                              val['close'],
                              val['pre_close'],
                              val['change'],
                              val['pct_chg'],
                              val['vol'],
                              val['amount'])
                    if conn.insert(sql) == 1:
                        print('MONTHLY record: %d-%s, insert successful' % (key, val['ts_code']))
                    else:
                        print('MONTHLY record: %d-%s, insert failure' % (key, val['ts_code']))
                        logto(logfile, 'MONTHLY record: %d-%s, insert failure. SQL: %s' % (key, val['ts_code'], sql))
                    conn.end(option='commit')
                break
        time.sleep(1.5)

    conn.end()
    conn.dispose()
