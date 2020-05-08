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
                                                        '%s_%s.txt' % (__name__, self.today)), 'info')
        self.dbconn = dbpool.MyPymysqlPool(self.logger, 'MysqlDatabaseInfo')

        if self.login_status:
            self.stock_and_index_list = list(self.getAllStocks().index)
        else:
            self.stock_and_index_list = []

    def insertQFQMinuteQuotationByDateRange(self, stock, start_date, end_date):
        table_name = 't_min_qfq_%s' % stock.split('.')[0]

        def __create_table():
            ret = self.dbconn.getAll(
                'select table_name from information_schema.tables where table_schema="quantification" and '
                'table_type="base table" and table_name="%s";' % table_name
            )
            if ret is None:
                return self.dbconn.common_execute(
                    'CREATE TABLE `%s` (`ts_code` varchar(128) NOT NULL COMMENT "tushare代码",`timestamp` '
                    'varchar(128) NOT NULL COMMENT "交易日期",`open` varchar(128) DEFAULT NULL COMMENT "开盘价",'
                    '`close` varchar(128) DEFAULT NULL,`low` varchar(128) DEFAULT NULL,`high` varchar(128) '
                    'DEFAULT NULL,`volume` varchar(128) DEFAULT NULL,`money` varchar(128) DEFAULT NULL,'
                    '`factor` varchar(128) DEFAULT NULL,`high_limit` varchar(128) DEFAULT NULL,`low_limit` '
                    'varchar(128) DEFAULT NULL,`avg` varchar(128) DEFAULT NULL,`pre_close` varchar(128) DEFAULT '
                    'NULL,`paused` varchar(128) DEFAULT NULL,`open_interest` varchar(128) DEFAULT NULL,'
                    'PRIMARY KEY (`ts_code`,`timestamp`) USING BTREE,KEY `UQ_TS_CODE` (`ts_code`),'
                    'KEY `UQ_TRADE_DATE` (`timestamp`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;' % table_name
                )
            return len(ret)

        if __create_table() < 1:
            self.logger.error('Not found table: %s or create it error' % table_name)
            return

        sql1 = 'INSERT INTO %s (ts_code, timestamp, `open`,' % table_name
        sql = sql1 + '`close`, low, high, volume, money, factor, high_limit, low_limit, avg, pre_close, paused, ' \
                     'open_interest)' \
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
    api = jqMinuteData('18780098283', 'Kangjing111', None)
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    # 240 * 300 * 15 * 200
    signal_15_years = 240 * 300
    start = '2019-01-01'
    end = '2020-05-07'

    for stock in api.stock_and_index_list:
        while True:
            if api.getCount() > signal_15_years:
                api.insertQFQMinuteQuotationByDateRange(stock, start, end)
                break
            else:
                api.logger.info('当日流量已用尽，等待第二天')
                time.sleep(3600)
