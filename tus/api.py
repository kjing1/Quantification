# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import tushare as ts
from utils import Retry
import time

MYTOKEN = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'


def init_tushare(logger, token):
    """
    初始化tushare
    :param logger: 日志对象
    :param token: token
    :return: tushare对象或None
    """
    try:
        ts.set_token(token)
        pro = ts.pro_api()
    except Exception as e:
        logger.error('INIT_TUSHARE executing get error: %s' % e)
        return None

    return pro


def insert_daliy_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    """
    通过tscode获取原始日行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
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
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_daliy_to_db_by_date(logger, pro, conn, tradedate, retry=3):
    """
    获取指定日期的所有股票原始行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param tradedate: 日期，格式为：20200101
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    df = Retry(pro.daily, logger, retry, trade_date=tradedate)
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
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_weekly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    """
    通过tscode获取原始周行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
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
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_weekly_to_db_by_date(logger, pro, conn, tradedate, retry=3):
    """
    获取指定日期的所有股票原始周行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param tradedate: 日期，格式为：20200101
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    df = Retry(pro.weekly, logger, retry, trade_date=tradedate,
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
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_monthly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
    """
    通过tscode获取原始月行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
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
                if conn.insert(sql) == 1:
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_monthly_to_db_by_date(logger, pro, conn, tradedate, retry=3):
    """
    获取指定日期的所有股票原始月行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param tradedate: 日期，格式为：20200101
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    df = Retry(pro.monthly, logger, retry, trade_date=tradedate,
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
            if conn.insert(sql) == 1:
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_stocks_base_info_to_db(logger, pro, conn, retry=3):
    """
    获取tushare中所有股票的基础信息
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库对象
    :param retry: 重试次数
    :return: 成功插入数据库的条数
    """
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
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def get_channel_chname(c):
    """
    返回渠道对应的中文名称
    :param c: 渠道英文名称
    :return: 渠道中文名称
    """
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
    """
    获取指定渠道的24H快讯
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：2020-01-01 23:11:11
    :param enddate: 结束日期，格式同startdate
    :param src: 渠道
    :param retry: 重试次数
    :return: 成功插入数据库的条数
    """
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
                                                     get_channel_chname(src),
                                                     time.time(),
                                                     val['content'].replace("\\", "\\\\").replace("'", "\\'").replace(
                                                         '"', '\\"'),
                                                     val['datetime'])
            if conn.insert(sql) == 1:
                logger.debug('%s : %d\'s news insert successful' % (__name__, key))
                cnt += 1
            else:
                logger.error('%s : %d\'s news insert failure, SQL: %s\n' % (__name__, key, sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_mojor_news_to_db(logger, pro, conn, startdate, enddate, src, retry=3):
    """
    获取长篇新闻
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：2020-01-01 23:11:11
    :param enddate: 结束日期，格式同startdate
    :param src: 渠道
    :param retry: 重试次数
    :return: 成功插入数据库的条数
    """
    cnt = 0
    df = Retry(pro.major_news,
               logger,
               retry, src=src, start_date=startdate, end_date=enddate, fields='title,content,pub_time,src')
    if df is not None:
        for key, val in df.iterrows():
            sql = 'INSERT INTO s_information (title, type, source, creat_date, content, pub_datetime) VALUES (' \
                  '"%s", "%s", "%s", "%s", "%s", "%s")' % (val['title'],
                                                         '新闻',
                                                         val['src'],
                                                         time.time(),
                                                         val['content'].replace("\\", "\\\\").replace("'",
                                                                                                      "\\'").replace(
                                                             '"', '\\"'),
                                                         val['pub_time'])
            if conn.insert(sql) == 1:
                logger.debug('%s : %d\'s news insert successful' % (__name__, key))
                cnt += 1
            else:
                logger.info('%s : %d\'s news insert failure' % (__name__, key))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_adj_factor_to_db_by_tscode(logger, pro, conn, tradedate, stocks_list, retry=3):
    """
    根据ts_code提取该股票所有日期的复权因子
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库对象
    :param tradedate: 可以指定日期，格式为：YYYYMMDD，也可以采用''提取全部日期
    :param stocks_list: ts_code列表
    :param retry: 重试次数
    :return: 成功插入数据库的条数
    """
    cnt = 0
    for stock in stocks_list:
        df = Retry(pro.adj_factor, logger, retry, ts_code=stock, trade_date=tradedate)
        if df is not None:
            for key, val in df.iterrows():
                sql = 'INSERT INTO t_adj_factor (ts_code, trade_date, adj_factor) VALUES ("%s", "%s", "%s")' % (
                    val['ts_code'],
                    val['trade_date'],
                    val['adj_factor']
                )
                if conn.insert(sql) == 1:
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_adj_factor_to_db_by_date(logger, pro, conn, tradedate, retry=3):
    """
    根据日期提取所有股票的复权因子
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库对象
    :param tradedate: 可以指定日期，格式为：YYYYMMDD，也可以采用''提取全部日期
    :param stocks_list: ts_code列表
    :param retry: 重试次数
    :return: 成功插入数据库的条数
    """
    cnt = 0
    df = Retry(pro.adj_factor, logger, retry, ts_code='', trade_date=tradedate)
    if df is not None:
        for key, val in df.iterrows():
            sql = 'INSERT INTO t_adj_factor (ts_code, trade_date, adj_factor) VALUES ("%s", "%s", "%s")' % (
                val['ts_code'],
                val['trade_date'],
                val['adj_factor']
            )
            if conn.insert(sql) == 1:
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_fq_daily_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, adj='qfq', asset='E', retry=3):
    """
    通过tscode获取复权的日行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param asset: None未复权 qfq前复权 hfq后复权 , 默认None
    :param adj: 资产类型，E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    for stock in stocks_list:
        df = Retry(ts.pro_bar, logger, retry,
                   ts_code=stock, start_date=startdate, end_date=enddate, adj=adj, asset=asset)
        if df is not None:
            for key, val in df.iterrows():
                sql = 'INSERT INTO t_daily_%s (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                      'pct_chg, vol, ' \
                      'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                          adj,
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
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_fq_weekly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, adj='qfq', asset='E', retry=3):
    """
    通过tscode获取复权的周行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param asset: None未复权 qfq前复权 hfq后复权 , 默认None
    :param adj: 资产类型，E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    for stock in stocks_list:
        df = Retry(ts.pro_bar, logger, retry,
                   ts_code=stock, start_date=startdate, end_date=enddate, adj=adj, asset=asset, freq='W')
        if df is not None:
            for key, val in df.iterrows():
                sql = 'INSERT INTO t_weekly_%s (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                      'pct_chg, vol, ' \
                      'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                          adj,
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
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_fq_monthly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, adj='qfq', asset='E', retry=3):
    """
    通过tscode获取复权的月行情
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param startdate: 开始日期，格式为：20200101
    :param enddate: 结束日期，格式同startdate
    :param stocks_list: 股票ts_code列表
    :param asset: None未复权 qfq前复权 hfq后复权 , 默认None
    :param adj: 资产类型，E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    for stock in stocks_list:
        df = Retry(ts.pro_bar, logger, retry,
                   ts_code=stock, start_date=startdate, end_date=enddate, adj=adj, asset=asset, freq='M')
        if df is not None:
            for key, val in df.iterrows():
                sql = 'INSERT INTO t_monthly_%s (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
                      'pct_chg, vol, ' \
                      'amount) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ' % (
                          adj,
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
                    logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                    cnt += 1
                else:
                    logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
            conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt


def insert_daily_index_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=3):
        """
        通过tscode获取每日指标
        :param logger: 日志对象
        :param pro: tushare对象
        :param conn: 数据库链接对象
        :param startdate: 开始日期，格式为：20200101
        :param enddate: 结束日期，格式同startdate
        :param stocks_list: 股票ts_code列表
        :param retry: 链接tushare重试次数，-1为一直重试
        :return: 成功插入数据库的数据条数
        """
        cnt = 0
        for stock in stocks_list:
            df = Retry(pro.daily_basic, logger, retry,
                       ts_code=stock,
                       trade_date='',
                       start_date=startdate,
                       end_date=enddate,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'turnover_rate,'
                              'turnover_rate_f,'
                              'volume_ratio,'
                              'pe,'
                              'pe_ttm,'
                              'pb,'
                              'ps,'
                              'ps_ttm,'
                              'dv_ratio,'
                              'dv_ttm,'
                              'total_share,'
                              'float_share,'
                              'free_share,'
                              'total_mv,'
                              'circ_mv')
            if df is not None:
                for key, val in df.iterrows():
                    sql = 'INSERT INTO t_daily_index (ts_code,' \
                          'trade_date,' \
                          'close,' \
                          'turnover_rate,' \
                          'turnover_rate_f,' \
                          'volume_ratio,' \
                          'pe,' \
                          'pe_ttm,' \
                          'pb,' \
                          'ps,' \
                          'ps_ttm,' \
                          'dv_ratio,' \
                          'dv_ttm,' \
                          'total_share,' \
                          'float_share,' \
                          'free_share,' \
                          'total_mv,' \
                          'circ_mv) VALUES' \
                          '("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", ' \
                          '"%s", "%s", "%s")' % \
                          (val['ts_code'],
                           val['trade_date'],
                           val['close'],
                           val['turnover_rate'],
                           val['turnover_rate_f'],
                           val['volume_ratio'],
                           val['pe'],
                           val['pe_ttm'],
                           val['pb'],
                           val['ps'],
                           val['ps_ttm'],
                           val['dv_ratio'],
                           val['dv_ttm'],
                           val['total_share'],
                           val['float_share'],
                           val['free_share'],
                           val['total_mv'],
                           val['circ_mv'])
                    if conn.insert(sql) == 1:
                        logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                        cnt += 1
                    else:
                        logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
                conn.end(option='commit')
        logger.info('%s all insert %d datas' % (__name__, cnt))
        return cnt


def insert_daily_index_to_db_by_date(logger, pro, conn, tradedate, retry=3):
    """
    通过日期获取每日指标
    :param logger: 日志对象
    :param pro: tushare对象
    :param conn: 数据库链接对象
    :param tradedate: 交易日期，格式为：20200101
    :param retry: 链接tushare重试次数，-1为一直重试
    :return: 成功插入数据库的数据条数
    """
    cnt = 0
    df = Retry(pro.daily_basic, logger, retry,
               ts_code='',
               trade_date=tradedate,
               start_date='',
               end_date='',
               fields='ts_code,'
                      'trade_date,'
                      'close,'
                      'turnover_rate,'
                      'turnover_rate_f,'
                      'volume_ratio,'
                      'pe,'
                      'pe_ttm,'
                      'pb,'
                      'ps,'
                      'ps_ttm,'
                      'dv_ratio,'
                      'dv_ttm,'
                      'total_share,'
                      'float_share,'
                      'free_share,'
                      'total_mv,'
                      'circ_mv')
    if df is not None:
        for key, val in df.iterrows():
            sql = 'INSERT INTO t_daily_index (ts_code,' \
                  'trade_date,' \
                  'close,' \
                  'turnover_rate,' \
                  'turnover_rate_f,' \
                  'volume_ratio,' \
                  'pe,' \
                  'pe_ttm,' \
                  'pb,' \
                  'ps,' \
                  'ps_ttm,' \
                  'dv_ratio,' \
                  'dv_ttm,' \
                  'total_share,' \
                  'float_share,' \
                  'free_share,' \
                  'total_mv,' \
                  'circ_mv) VALUES' \
                  '("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", ' \
                  '"%s", "%s", "%s")' % \
                  (val['ts_code'],
                   val['trade_date'],
                   val['close'],
                   val['turnover_rate'],
                   val['turnover_rate_f'],
                   val['volume_ratio'],
                   val['pe'],
                   val['pe_ttm'],
                   val['pb'],
                   val['ps'],
                   val['ps_ttm'],
                   val['dv_ratio'],
                   val['dv_ttm'],
                   val['total_share'],
                   val['float_share'],
                   val['free_share'],
                   val['total_mv'],
                   val['circ_mv'])
            if conn.insert(sql) == 1:
                logger.debug('%s : %d-%s insert successful' % (__name__, key, val['ts_code']))
                cnt += 1
            else:
                logger.error('%s : %d-%s insert failure. SQL: %s' % (__name__, key, val['ts_code'], sql))
        conn.end(option='commit')
    logger.info('%s all insert %d datas' % (__name__, cnt))
    return cnt
