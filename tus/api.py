# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import tushare as ts
from utils import Retry, RetryDecorator
import time

MYTOKEN = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'


def init_tushare(logger, token):
    try:
        ts.set_token(token)
        pro = ts.pro_api()
    except Exception as e:
        logger.error('INIT_TUSHARE executing get error: %s' % e)
        return None

    return pro


def insert_daliy_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    cnt = 0
    for stock in stocks_list:
        df = Retry(pro.daily, logger, retry, ts_code=stock, start_date=startdate, end_date=enddate)
        if df is not None:
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
                    logger.info('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_weekly_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    cnt = 0
    for stock in stocks_list:
        df = Retry(pro.weekly, logger, retry, ts_code=stock, start_date=startdate, end_date=enddate,
                   fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        if df is not None:
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
                    logger.info('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_monthly_to_db(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    cnt = 0
    for stock in stocks_list:
        df = Retry(pro.monthly, logger, retry, ts_code=stock, start_date=startdate, end_date=enddate,
                   fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        if df is not None:
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
                if conn.debug(sql) == 1:
                    logger.info('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_stocks_base_info_to_db(logger, pro, conn, retry=3):
    cnt = 0
    df = Retry(pro.stock_basic,
               logger,
               retry,
               exchange='',
               list_status='',
               fields='ts_code,'
                      'symbol,'
                      'name,'
                      'area,'
                      'industry,'
                      'list_date,'
                      'fullname,'
                      'enname,'
                      'market,'
                      'exchange,'
                      'curr_type,'
                      'list_status,'
                      'delist_date,'
                      'is_hs')
    if df is not None:
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
                logger.info('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def get_channel_chname(c):
    if c.lower() == 'sina':
        return '新浪财经'
    elif c.lower() == 'wallstreetcn':
        return '华尔街见闻'
    elif c.lower() == '10jqka':
        return '同花顺'
    elif c.lower() == 'eastmoney':
        return '东方财富'
    elif c.lower() == 'yuncaijing':
        return '云财经'
    else:
        return c


def insert_flash_news_to_db(logger, pro, conn, startdate, enddate, src, retry=3):
    cnt = 0
    df = Retry(pro.news,
               logger,
               retry, src=src, start_date=startdate, end_date=enddate, fields='title,content,datetime,channels')
    if df is not None:
        for key, val in df.iterrows():
            try:
                cls = '%s' % val['channels'][0]['name']
            except Exception as e:
                cls = '其他'
            sql = 'INSERT INTO s_flash_news (type, source, creat_date, content, pub_datetime) VALUES (' \
                  '"%s", "%s", "%s", "%s", "%s")' % (cls,
                                                     get_channel_chname(c),
                                                     time.time(),
                                                     val['content'].replace("\\", "\\\\").replace("'","\\'").replace('"', '\\"'),
                                                     val['datetime'])
            if conn.insert(sql) == 1:
                logger.info('%s : %d\'s news insert successful' % (__name__, key))
                cnt += 1
            else:
                logger.error('%s : %d\'s news insert failure, SQL: %s\n' % (__name__, key, sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_mojor_news_to_db(logger, pro, conn, startdate, enddate, src, retry=3):
    cnt = 0
    df = Retry(pro.major_news,
               logger,
               retry, src=src, start_date=startdate, end_date=enddate, fields='title,content,pub_time,src')
    if df is not None:
        for key, val in df.iterrows():
            sql = 'INSERT INTO s_major_news (title, type, source, creat_date, content, pub_datetime) VALUES (' \
                  '"%s", %s, "%s", "%s", "%s", "%s")' % (val['title'],
                                                         '新闻',
                                                         val['src'],
                                                         time.time(),
                                                         val['content'].replace("\\", "\\\\").replace("'","\\'").replace('"', '\\"'),
                                                         val['pub_time'])
            if conn.insert(sql) == 1:
                logger.info('%s : %d\'s news insert successful' % (__name__, key))
                cnt += 1
            else:
                logger.info('%s : %d\'s news insert failure' % (__name__, key))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt