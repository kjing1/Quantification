# python 3.7.4
# coding = utf-8
# filename t_daily_t_daily_index_sync.py
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

logdir = '/opt/quantification/logs'

if __name__ == '__main__':
    stocks_list = []
    threads_list = []
    cnt = 0
    # 初始化日志
    if not os.path.exists(os.path.expanduser(logdir)):
        os.mkdir(os.path.expanduser(logdir))
    logger = log.init_logging(
        os.path.join(os.path.expanduser(logdir), '%s_%s.txt' % ('sync',
                                                                time.strftime('%Y%m%d',
                                                                              time.localtime(time.time())))),
        'info')
    conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo')
    # 获取股票ts代码
    for d in conn.getAll('select ts_code from t_stocks'):
        stocks_list.append(d['ts_code'])

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    logger.info('-------------%s begin-------------')
    logger.info('All %d stocks' % len(stocks_list))

    for stock in stocks_list:
        logger.info('Get trade_date from %s' % stock)
        daily_datas = conn.getAll('SELECT ts_code, trade_date from t_daily where ts_code="%s"' % stock)
        logger.debug('%d datas' % len(daily_datas))
        for data in daily_datas:
            logger.info('Get index data by %s-%s' % (data['ts_code'], data['trade_date']))
            index_datas = conn.getAll('SELECT * from t_daily_index where ts_code="%s" and trade_date="%s"' %
                                      (data['ts_code'], data['trade_date']))
            logger.debug('%d index datas' % len(index_datas))
            if len(index_datas) != 1:
                logger.error('Index data error')
                continue
            up = 'UPDATE t_daily SET ' \
                 'turnover_rate = "%s",' \
                 'turnover_rate_f= "%s",' \
                 'volume_ratio = "%s",' \
                 'pe = "%s",' \
                 'pe_ttm = "%s",' \
                 'pb = "%s",' \
                 'ps = "%s",' \
                 'ps_ttm = "%s",' \
                 'dv_ratio = "%s",' \
                 'dv_ttm = "%s",' \
                 'total_share = "%s",' \
                 'float_share = "%s",' \
                 'free_share = "%s",' \
                 'total_mv = "%s",' \
                 'circ_mv = "%s" ' \
                 'WHERE ts_code="%s" and trade_date="%s"' % (index_datas[0]['turnover_rate'],
                                                             index_datas[0]['turnover_rate_f'],
                                                             index_datas[0]['volume_ratio'],
                                                             index_datas[0]['pe'],
                                                             index_datas[0]['pe_ttm'],
                                                             index_datas[0]['pb'],
                                                             index_datas[0]['ps'],
                                                             index_datas[0]['ps_ttm'],
                                                             index_datas[0]['dv_ratio'],
                                                             index_datas[0]['dv_ttm'],
                                                             index_datas[0]['total_share'],
                                                             index_datas[0]['float_share'],
                                                             index_datas[0]['free_share'],
                                                             index_datas[0]['total_mv'],
                                                             index_datas[0]['circ_mv'],
                                                             data['ts_code'],
                                                             data['trade_date'])
            logger.debug('SQL: %s' % up)

            if conn.update(up) == 1:
                cnt += 1
            else:
                logger.error('Update error, SQL: %s' % up)

    logger.info('All updated %d datas' % cnt)
    conn.dispose()
