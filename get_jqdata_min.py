# python 3.7.4
# coding = utf-8
# filename tus_batch_business.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from jqdata import api
from db import dbpool
import os
import log
import time


class jqMinuteData(api.jqdataApi):
    def __init__(self, account, password, logger, logdir='./logs/'):
        super().__init__(account, password)

        self.today = time.strftime('%Y%m%d', time.localtime(time.time()))

        if logger is not None:
            self.logger = logger
        else:
            self.logger = log.init_logging(os.path.join(os.path.expanduser(logdir),
                                                        'minute_%s_%s.txt' % (__name__, self.today)), 'info')
        self.dbconn = dbpool.MyPymysqlPool(self.logger, 'MysqlDatabaseInfo')

        if self.login_status:
            self.stock_and_index_list = list(self.getAllStocks().index)
        else:
            self.stock_and_index_list = []

    def insertQFQMinuteQuotationByDateRange(self, stock, start_date, end_date):
        sql = 'INSERT INTO t_min_qfq (ts_code, timestamp, `open`,' \
              '`close`, low, high, volume, money, factor, high_limit, low_limit, avg, pre_close, paused, open_interest)' \
              ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getSignalStockMinuteQuotationByDateRange(stock, start_date, end_date, fq='pre')
        if df is not None:
            for key, val in df.iterrows():
                values.append([stock,
                               str(key),
                               val['open'],
                               val['close'],
                               val['low'],
                               val['high'],
                               val['volume'],
                               val['money'],
                               val['factor'],
                               val['high_limit'],
                               val['low_limit'],
                               val['avg'],
                               val['pre_close'],
                               val['paused'],
                               val['open_interest']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('%s insert %d datas' % (stock, ret))
            else:
                self.logger.error('%s insert data to database failure, all %d errors' % (stock, len(values)))
        else:
            self.logger.error('[getSignalStockMinuteQuotationByDateRange] -> get None')


if __name__ == '__main__':
    api = jqMinuteData('18780098283', 'Kj_459951958', None)
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    # 240 * 300 * 15 * 200
    signal_15_years = 240 * 300 * 15
    start = '2005-01-01'
    end = '2020-04-30'

    for stock in api.stock_and_index_list:
        while True:
            if api.getCount() > signal_15_years:
                api.insertQFQMinuteQuotationByDateRange(stock, start, end)
                break
            else:
                api.logger.info('当日流量已用尽，等待第二天')
                time.sleep(3600)
