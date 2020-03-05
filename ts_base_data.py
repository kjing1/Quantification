# python 3.7.4
# coding = utf-8
# filename ts_base_data.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from db import dbpool
import time
import log
import tus.api as tsapi
import threading
import argparse
import sys
import os


# 获取前复权日行情
def qfq_daily(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的前复权日行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_daily_to_db_by_tscode(logger, pro, conn,
                                                startdate, enddate, stocks_list, adj='qfq', asset='E', retry=retry)
    logger.info('前复权日行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取后复权日行情
def hfq_daily(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的后复权日行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_daily_to_db_by_tscode(logger, pro, conn,
                                                startdate, enddate, stocks_list, adj='hfq', asset='E', retry=retry)
    logger.info('后复权日行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取前复权周行情
def qfq_weekly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的前复权周行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_weekly_to_db_by_tscode(logger, pro, conn,
                                                 startdate, enddate, stocks_list, adj='qfq', asset='E', retry=retry)
    logger.info('前复权周行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取后复权周行情
def hfq_weekly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的后复权周行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_weekly_to_db_by_tscode(logger, pro, conn,
                                                 startdate, enddate, stocks_list, adj='hfq', asset='E', retry=retry)
    logger.info('后复权周行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取前复权月行情
def qfq_monthly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的前复权月行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_monthly_to_db_by_tscode(logger, pro, conn,
                                                  startdate, enddate, stocks_list, adj='qfq', asset='E', retry=retry)
    logger.info('前复权月行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取后复权月行情
def hfq_monthly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的后复权月行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_fq_monthly_to_db_by_tscode(logger, pro, conn,
                                                  startdate, enddate, stocks_list, adj='hfq', asset='E', retry=retry)
    logger.info('后复权月行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取日行情
def daily(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的原始日行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_daliy_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=retry)
    logger.info('原始日行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取周行情
def weekly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的原始周行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_weekly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=retry)
    logger.info('原始周行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取月行情
def monthly(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的原始月行情数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_monthly_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=retry)
    logger.info('原始月行情数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取每日指标
def tsindex(logger, pro, conn, stocks_list, startdate, enddate, retry):
    now = time.time()
    logger.info('获取%d只股票从 %s 到 %s 的每日指标数据' % (len(stocks_list), startdate, enddate))
    ret = tsapi.insert_daily_index_to_db_by_tscode(logger, pro, conn, startdate, enddate, stocks_list, retry=retry)
    logger.info('指标数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


# 获取复权因子
def adj_factor(logger, pro, conn, stocks_list, retry):
    now = time.time()
    logger.info('获取 %d 只股票的复权因子' % len(stocks_list))
    ret = tsapi.insert_adj_factor_to_db_by_tscode(logger, pro, conn, '', stocks_list, retry=retry)
    logger.info('复权因子数据拉取完成，共插入数据库 %d 条，耗时 %d 秒' % (ret, time.time() - now))
    conn.dispose()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--daily_quotation', type=bool,
                        help='Get daily quotation from tushare, default: True', default=False)
    parser.add_argument('--weekly_quotation', type=bool,
                        help='Get weekly quotation from tushare, default: True', default=False)
    parser.add_argument('--monthly_quotation', type=bool,
                        help='Get monthly quotation from tushare, default: True', default=False)
    parser.add_argument('--qfq_daily_quotation', type=bool,
                        help='Get qfq daily quotation from tushare, default: True', default=False)
    parser.add_argument('--hfq_daily_quotation', type=bool,
                        help='Get hfq daily quotation from tushare, default: True', default=False)
    parser.add_argument('--qfq_weekly_quotation', type=bool,
                        help='Get qfq weekly quotation from tushare, default: True', default=False)
    parser.add_argument('--hfq_weekly_quotation', type=bool,
                        help='Get hfq weekly quotation from tushare, default: True', default=False)
    parser.add_argument('--qfq_monthly_quotation', type=bool,
                        help='Get qfq monthly quotation from tushare, default: True', default=False)
    parser.add_argument('--hfq_monthly_quotation', type=bool,
                        help='Get hfq monthly quotation from tushare, default: True', default=False)
    parser.add_argument('--daily_index', type=bool,
                        help='Get daily index from tushare, default: True', default=False)
    parser.add_argument('--adj_factor', type=bool,
                        help='Get adjust factor, default: False', default=False)
    parser.add_argument('--logdir', type=str,
                        help='Log directory, default: /opt/quantification/logs', default='/opt/quantification/logs')
    parser.add_argument('--loglevel', type=str,
                        help='Log level, default: info', default='info')
    parser.add_argument('--startdate', type=str,
                        help='Start date, default: today', default='')
    parser.add_argument('--enddate', type=str,
                        help='End date, default: today', default='')
    parser.add_argument('--retry', type=int,
                        help='Exception retry times, default: 3', default=3)
    return parser.parse_args(argv)


def mymain(args):
    stocks_list = []
    threads_list = []
    # 初始化日志
    if not os.path.exists(os.path.expanduser(args.logdir)):
        os.mkdir(os.path.expanduser(args.logdir))
    logger = log.init_logging(
        os.path.join(os.path.expanduser(args.logdir), '%s_%s.txt' % (__name__,
                                                                     time.strftime('%Y%m%d',
                                                                                   time.localtime(time.time())))),
        args.loglevel)
    # 初始化tushare
    pro = tsapi.init_tushare(logger, tsapi.MYTOKEN)
    if pro is None:
        print('Init tushare error, exit')
        exit(1)
    # 链接数据库
    conn_tmp = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
    # 获取股票ts代码
    for d in conn_tmp.getAll('select ts_code from t_stocks'):
        stocks_list.append(d['ts_code'])
    conn_tmp.dispose()

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    if args.startdate == '':
        startdate = today
        enddate = today
    else:
        startdate = args.startdate
        enddate = args.enddate

    # 日行情线程
    if args.daily_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_daily = threading.Thread(target=daily,
                                       args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_daily.start()
        except Exception as e:
            logger.error('启动日行情线程失败: %s' % e)
        else:
            threads_list.append(t_daily)

    # 周行情线程
    if args.weekly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_weekly = threading.Thread(target=weekly,
                                        args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_weekly.start()
        except Exception as e:
            logger.error('启动周行情线程失败: %s' % e)
        else:
            threads_list.append(t_weekly)

    # 月行情线程
    if args.monthly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_monthly = threading.Thread(target=monthly,
                                         args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_monthly.start()
        except Exception as e:
            logger.error('启动月行情线程失败: %s' % e)
        else:
            threads_list.append(t_monthly)

    # 前复权日行情线程
    if args.qfq_daily_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_qfq_daily = threading.Thread(target=qfq_daily,
                                           args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_qfq_daily.start()
        except Exception as e:
            logger.error('启动前复权日行情线程失败: %s' % e)
        else:
            threads_list.append(t_qfq_daily)

    # 前复权周行情线程
    if args.qfq_weekly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_qfq_weekly = threading.Thread(target=qfq_weekly,
                                            args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_qfq_weekly.start()
        except Exception as e:
            logger.error('启动前复权周行情线程失败: %s' % e)
        else:
            threads_list.append(t_qfq_weekly)

    # 前复权月行情线程
    if args.qfq_monthly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_qfq_monthly = threading.Thread(target=qfq_monthly,
                                             args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_qfq_monthly.start()
        except Exception as e:
            logger.error('启动前复权月行情线程失败: %s' % e)
        else:
            threads_list.append(t_qfq_monthly)

    # 后复权日行情线程
    if args.hfq_daily_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_hfq_daily = threading.Thread(target=hfq_daily,
                                           args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_hfq_daily.start()
        except Exception as e:
            logger.error('启动后复权日行情线程失败: %s' % e)
        else:
            threads_list.append(t_hfq_daily)

    # 后复权周行情线程
    if args.hfq_weekly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_hfq_weekly = threading.Thread(target=hfq_weekly,
                                            args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_hfq_weekly.start()
        except Exception as e:
            logger.error('启动后复权周行情线程失败: %s' % e)
        else:
            threads_list.append(t_hfq_weekly)

    # 后复权月行情线程
    if args.hfq_monthly_quotation:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_hfq_monthly = threading.Thread(target=hfq_monthly,
                                             args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_hfq_monthly.start()
        except Exception as e:
            logger.error('启动后复权月行情线程失败: %s' % e)
        else:
            threads_list.append(t_hfq_monthly)

    # 每日指标线程
    if args.daily_index:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_index = threading.Thread(target=tsindex,
                                       args=(logger, pro, conn, stocks_list, startdate, enddate, args.retry))
            t_index.start()
        except Exception as e:
            logger.error('启动每日指标线程失败: %s' % e)
        else:
            threads_list.append(t_index)

    # 复权因子线程
    if args.adj_factor:
        conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
        try:
            t_adj = threading.Thread(target=adj_factor,
                                     args=(logger,
                                           pro,
                                           conn,
                                           stocks_list,
                                           args.retry))
            t_adj.start()
        except Exception as e:
            logger.error('启动复权因子线程失败: %s' % e)
        else:
            threads_list.append(t_adj)

    def _continueloop(threads):
        for t in threads:
            if t.is_alive():
                return True
        return False

    now = time.time()
    print('\t\t\t\t%s begin' % time.strftime('%Y%m%d %H%M%S', time.localtime(now)))
    while _continueloop(threads_list):
        print('\r<%08d>s [\\], see log to more information' % (time.time() - now), end='')
        time.sleep(0.1)
        print('\r<%08d>s [/], see log to more information' % (time.time() - now), end='')
        time.sleep(0.1)
    print('\n\t\t\t\tAll complete, done')


if __name__ == '__main__':
    mymain(parse_arguments(sys.argv[1:]))
