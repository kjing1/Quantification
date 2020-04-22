# python 3.7.4
# coding = utf-8
# filename tus_batch_business.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from tus.api import tusApi, MYTOKEN
from db import dbpool
import os
import log
import time
import threading
import argparse
import sys


class batchBusiness(tusApi):
    def __init__(self, start, end, trade_date='', logger=None, logdir='.\\logs\\', retry=5, timeout=30, intv=0.5):
        super().__init__(MYTOKEN, retry=retry, timeout=timeout, intv=intv)
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        if logger is None:
            self.logger = log.init_logging(os.path.join(os.path.expanduser(logdir),
                                                        '%s_%s.txt' % (__name__, today)), 'info')
        else:
            self.logger = logger
        self.dbconn = dbpool.MyPymysqlPool(self.logger, 'MysqlDatabaseInfo')
        self.stock_list = []
        self.index_list = []
        if start == '':
            self.start_date = today
        else:
            self.start_date = start
        if end == '':
            self.end_date = today
        else:
            self.end_date = end
        self.market = ['MSCI', 'CSI', 'SSE', 'SZSE', 'CICC', 'SW', 'OTH']
        if trade_date == '':
            self.trade_date = today
        else:
            self.trade_date = trade_date

        self.getAllStockCodeFromDatabase()
        self.getAllIndexCodeFromDatabase()

    def insertStockBaseInformationToDatabase(self):
        sql = 'INSERT INTO t_stocks (ts_code,' \
              ' code,' \
              ' name,' \
              ' area,' \
              ' industry,' \
              ' fullname,' \
              ' enname,' \
              ' market,' \
              ' exchange,' \
              ' curr_type,' \
              ' status,' \
              ' date,' \
              ' de_date,' \
              ' is_hs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        df = self.getAllStockBaseInformation()
        if df is None:
            self.logger.error('[getAllStockBaseInformation] -> get None, retry')
        else:
            for key, val in df.iterrows():
                values = [[val['ts_code'],
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
                           val['is_hs']]]
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.info('insert %d data to database' % ret)
                else:
                    self.logger.warning('insert to database may be some errors, all insert %d' % ret)

    def getAllIndexCodeFromDatabase(self):
        all_fetched = self.dbconn.getAll('SELECT ts_code FROM t_index_base')
        if all_fetched is not None:
            for d in all_fetched:
                self.index_list.append(d['ts_code'])
        else:
            self.logger.warning('get None')

    def getAllStockCodeFromDatabase(self):
        all_fetched = self.dbconn.getAll('SELECT ts_code FROM t_stocks')
        if all_fetched is not None:
            for d in all_fetched:
                self.stock_list.append(d['ts_code'])
        else:
            self.logger.warning('get None')

    def insertDailyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_daily (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockDailyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s all insert %d datas' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockDailyQuantByDate] -> %s get None' % stock_code)

        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertDailyQuantToDatabaseByDate(self):
        sql = 'INSERT INTO t_daily (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockDailyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('all insert %d datas' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.warning('[getAllStockDailyQuantByDate] -> get None')

    def insertWeeklyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_weekly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stocks_list:
            values = []
            df = self.getSignalStockWeeklyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to databases' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockWeeklyQuantByDate] -> %s get None' % stock_code)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertWeeklyQuantToDatabaseByDate(self):
        sql = 'INSERT INTO t_weekly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockWeeklyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to databases' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockWeeklyQuantByDate] -> get None')

    def insertMonthlyQuantToDatabasebyDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_monthly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stocks_list:
            values = []
            df = self.getSignalStockMonthlyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockMonthlyQuantByDate] -> %s get None' % stock_code)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertMonthlyQuantToDatabaseByDate(self):
        values = []
        sql = 'INSERT INTO t_monthly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        df = self.getAllStockMonthlyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockMonthlyQuantByDate] -> get None')

    def insert24HFlashNewsToDatabase(self):
        src = ['sina', 'wallstreetcn', '10jqka', 'eastmoney', 'yuncaijing']

        def __get_channel_chname(c):
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

        count = 0
        err = 0
        sql = 'INSERT INTO t_flash_news (type, source, creat_date, content, pub_datetime) VALUES (' \
              '%s, %s, %s, %s, %s)'
        cls = ''
        for s in src:
            values = []
            df = self.get24HFlashNews(s,
                                      '%s-%s-%s 00:00:00' % (self.start_date[0:4],
                                                             self.start_date[4:6],
                                                             self.start_date[6:8]),
                                      '%s-%s-%s 23:59:59' % (self.end_date[0:4],
                                                             self.end_date[4:6],
                                                             self.end_date[6:8]))
            if df is not None:
                for key, val in df.iterrows():
                    try:
                        cls = '%s' % val['channels'][0]['name']
                    except Exception as e:
                        cls = '其他'
                    finally:
                        values.append([cls,
                                       __get_channel_chname(s),
                                       time.time(),
                                       val['content'].replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"'),
                                       val['datetime']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('insert %d flash news to database, src: %s' % (ret, __get_channel_chname(s)))
                    count += ret
                else:
                    self.logger.error('insert flash news to database get some error: %d, '
                                      'src: %s' % (ret, __get_channel_chname(s)))
                    err += len(values)
            else:
                self.logger.error('[get24HFlashNews] -> src: %s get None' % __get_channel_chname(s))
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertMojorNewsToDatabase(self):
        sql = 'INSERT INTO t_information (title, type, source, creat_date, content, pub_datetime) VALUES (' \
              '%s, %s, %s, %s, %s, %s)'
        df = self.getMajorNews('%s-%s-%s 00:00:00' % (self.start_date[0:4],
                                                      self.start_date[4:6],
                                                      self.start_date[6:8]),
                               '%s-%s-%s 23:59:59' % (self.end_date[0:4],
                                                      self.end_date[4:6],
                                                      self.end_date[6:8]))
        values = []
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['title'],
                               '新闻',
                               val['src'],
                               time.time(),
                               val['content'].replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"'),
                               val['pub_time']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getMajorNews] -> get None')

    def insertAdjFactorToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_adj_factor (ts_code, trade_date, adj_factor) VALUES (%s, %s, %s)'
        for stock_code in self.stocks_list:
            values = []
            df = self.getSignalStockAdjFactorByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['adj_factor']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockAdjFactorByDate] -> get None')
        self.logger.info('all insert %d datas and %d errors' % (count, err))

    def insertAdjFactorToDatabaseByDate(self):
        sql = 'INSERT INTO t_adj_factor (ts_code, trade_date, adj_factor) VALUES (%s, %s, %s)'
        df = self.getAllStockAdjFactorByDate(self.trade_date)
        values = []
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['adj_factor']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockAdjFactorByDate] -> get None')

    def insertQfqDailyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_daily_qfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockQFQDailyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockQFQDailyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertHfqDailyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_daily_hfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockHFQDailyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockHFQDailyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertQfqWeeklyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_weekly_qfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockQFQWeeklyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockQFQWeeklyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertHfqWeeklyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_weekly_hfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockHFQWeeklyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockHFQWeeklyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertQfqMonthlyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_monthly_qfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockQFQMonthlyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockQFQMonthlyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertHfqMonthlyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_monthly_hfq (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, ' \
              'amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockHFQMonthlyQuantByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockHFQMonthlyQuantByDate] -> get None')
            # tushare pro_bar interface limits 1000t/min
            time.sleep(1)
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertDailyIndexToDatabaseByDateRange(self):
        count = 0
        err = 0
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
              '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s)'
        for stock_code in self.stocks_list:
            values = []
            df = self.getSignalStockDailyIndexByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
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
                                   val['circ_mv']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockDailyIndexByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertDailyIndexToDatabaseByDate(self):
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
              '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s)'
        df = self.getAllStockDailyIndexByDate(self.trade_date)
        values = []
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
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
                               val['circ_mv']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockDailyIndexByDate] -> get None')

    def insertCompanyBaseInformationToDatabaseByExchange(self):
        exc = ['SSE', 'SZSE']
        count = 0
        err = 0
        sql = 'INSERT INTO t_company_base_info (ts_code,' \
              ' exchange,' \
              ' chairman,' \
              ' manager,' \
              ' secretary,' \
              ' reg_capital,' \
              ' setup_date,' \
              ' province,' \
              ' city,' \
              ' introduction,' \
              ' website,' \
              ' email,' \
              ' office,' \
              ' employees,' \
              ' main_business,' \
              ' business_scope) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for e in exc:
            df = self.getCompanyBaseInformationByExchange(e)
            if df is not None:
                for key, val in df.iterrows():
                    values = [[val['ts_code'],
                               val['exchange'],
                               val['chairman'],
                               val['manager'],
                               val['secretary'],
                               val['reg_capital'],
                               val['setup_date'],
                               val['province'],
                               val['city'],
                               val['introduction'],
                               val['website'],
                               val['email'],
                               val['office'],
                               val['employees'],
                               val['main_business'],
                               val['business_scope']]]
                    ret = self.dbconn.insertMany(sql, values)
                    if ret == len(values):
                        self.logger.debug('%s insert %d datas to database' % (e, ret))
                        count += ret
                    else:
                        self.logger.error('%s insert data to database get some error: %d' % (e, ret))
                        err += len(values)
            else:
                self.logger.error('[getCompanyBaseInformationByExchange] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertSuspendStocksInformationToDatabaseByDate(self):
        sql = 'INSERT INTO t_suspend (ts_code, trade_date, suspend_timing, suspend_type) VALUES (%s, %s, %s, %s)'
        df = self.getSuspendStocksByDate(self.trade_date)
        values = []
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['suspend_timing'],
                               val['suspend_type']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getSuspendStocksByDate] -> get None')

    def insertRestartStocksInformationToDatabaseByDate(self):
        sql = 'INSERT INTO t_suspend (ts_code, trade_date, suspend_timing, suspend_type) VALUES (%s, %s, %s, %s)'
        df = self.getRestartStocksByDate(self.trade_date)
        values = []
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['suspend_timing'],
                               val['suspend_type']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getRestartStocksByDate] -> get None')

    def insertStocksMoneyFlowToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_money_flow (ts_code,' \
              ' trade_date,' \
              ' buy_sm_vol,' \
              ' buy_sm_amount,' \
              ' sell_sm_vol,' \
              ' sell_sm_amount,' \
              ' buy_md_vol,' \
              ' buy_md_amount,' \
              ' sell_md_vol,' \
              ' sell_md_amount,' \
              ' buy_lg_vol,' \
              ' buy_lg_amount,' \
              ' sell_lg_vol,' \
              ' sell_lg_amount,' \
              ' buy_elg_vol,' \
              ' buy_elg_amount,' \
              ' sell_elg_vol,' \
              ' sell_elg_amount,' \
              ' net_mf_vol,' \
              ' net_mf_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockMoneyFlowByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['buy_sm_vol'],
                                   val['buy_sm_amount'],
                                   val['sell_sm_vol'],
                                   val['sell_sm_amount'],
                                   val['buy_md_vol'],
                                   val['buy_md_amount'],
                                   val['sell_md_vol'],
                                   val['sell_md_amount'],
                                   val['buy_lg_vol'],
                                   val['buy_lg_amount'],
                                   val['sell_lg_vol'],
                                   val['sell_lg_amount'],
                                   val['buy_elg_vol'],
                                   val['buy_elg_amount'],
                                   val['sell_elg_vol'],
                                   val['sell_elg_amount'],
                                   val['net_mf_vol'],
                                   val['net_mf_amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s inseret data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockMoneyFlowByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksMoneyFlowToDatabaseByDate(self):
        sql = 'INSERT INTO t_money_flow (ts_code,' \
              ' trade_date,' \
              ' buy_sm_vol,' \
              ' buy_sm_amount,' \
              ' sell_sm_vol,' \
              ' sell_sm_amount,' \
              ' buy_md_vol,' \
              ' buy_md_amount,' \
              ' sell_md_vol,' \
              ' sell_md_amount,' \
              ' buy_lg_vol,' \
              ' buy_lg_amount,' \
              ' sell_lg_vol,' \
              ' sell_lg_amount,' \
              ' buy_elg_vol,' \
              ' buy_elg_amount,' \
              ' sell_elg_vol,' \
              ' sell_elg_amount,' \
              ' net_mf_vol,' \
              ' net_mf_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockMoneyFlowByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['buy_sm_vol'],
                               val['buy_sm_amount'],
                               val['sell_sm_vol'],
                               val['sell_sm_amount'],
                               val['buy_md_vol'],
                               val['buy_md_amount'],
                               val['sell_md_vol'],
                               val['sell_md_amount'],
                               val['buy_lg_vol'],
                               val['buy_lg_amount'],
                               val['sell_lg_vol'],
                               val['sell_lg_amount'],
                               val['buy_elg_vol'],
                               val['buy_elg_amount'],
                               val['sell_elg_vol'],
                               val['sell_elg_amount'],
                               val['net_mf_vol'],
                               val['net_mf_amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('inseret data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockMoneyFlowByDate] -> get None')

    def insertStocksLimitPriceToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_limit_price (ts_code,' \
              ' trade_date,' \
              ' pre_close,' \
              ' up_limit,' \
              ' down_limit) VALUES (%s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockLimitPriceByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['pre_close'],
                                   val['up_limit'],
                                   val['down_limit']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockLimitPriceByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksLimitPriceToDatabaseByDate(self):
        sql = 'INSERT INTO t_limit_price (ts_code,' \
              ' trade_date,' \
              ' pre_close,' \
              ' up_limit,' \
              ' down_limit) VALUES (%s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockLimitPriceByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['pre_close'],
                               val['up_limit'],
                               val['down_limit']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockLimitPriceByDate] -> get None')

    def insertLimitUpStocksToDatabaseByDate(self):
        sql = 'INSERT INTO t_limit_stocks (ts_code,' \
              ' trade_date,' \
              ' name,' \
              ' close,' \
              ' pct_chg,' \
              ' amp,' \
              ' fc_ratio,' \
              ' fl_ratio,' \
              ' fd_amount,' \
              ' first_time,' \
              ' last_time,' \
              ' open_times,' \
              ' strth,' \
              ' `limit`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockLimitUpStocksByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['name'],
                               val['close'],
                               val['pct_chg'],
                               val['amp'],
                               val['fc_ratio'],
                               val['fl_ratio'],
                               val['fd_amount'],
                               val['first_time'],
                               val['last_time'],
                               val['open_times'],
                               val['strth'],
                               val['limit']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockLimitUpStocksByDate] -> get None')

    def insertLimitUpStocksToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_limit_stocks (ts_code,' \
              ' trade_date,' \
              ' name,' \
              ' close,' \
              ' pct_chg,' \
              ' amp,' \
              ' fc_ratio,' \
              ' fl_ratio,' \
              ' fd_amount,' \
              ' first_time,' \
              ' last_time,' \
              ' open_times,' \
              ' strth,' \
              ' `limit`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        count = 0
        err = 0
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockLimitUpStocksByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['name'],
                                   val['close'],
                                   val['pct_chg'],
                                   val['amp'],
                                   val['fc_ratio'],
                                   val['fl_ratio'],
                                   val['fd_amount'],
                                   val['first_time'],
                                   val['last_time'],
                                   val['open_times'],
                                   val['strth'],
                                   val['limit']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockLimitUpStocksByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertLimitDownStocksToDatabaseByDate(self):
        sql = 'INSERT INTO t_limit_stocks (ts_code,' \
              ' trade_date,' \
              ' name,' \
              ' close,' \
              ' pct_chg,' \
              ' amp,' \
              ' fc_ratio,' \
              ' fl_ratio,' \
              ' fd_amount,' \
              ' first_time,' \
              ' last_time,' \
              ' open_times,' \
              ' strth,' \
              ' `limit`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockLimitDownStocksByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['name'],
                               val['close'],
                               val['pct_chg'],
                               val['amp'],
                               val['fc_ratio'],
                               val['fl_ratio'],
                               val['fd_amount'],
                               val['first_time'],
                               val['last_time'],
                               val['open_times'],
                               val['strth'],
                               val['limit']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockLimitDownStocksByDate] -> get None')

    def insertLimitDownStocksToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_limit_stocks (ts_code,' \
              ' trade_date,' \
              ' name,' \
              ' close,' \
              ' pct_chg,' \
              ' amp,' \
              ' fc_ratio,' \
              ' fl_ratio,' \
              ' fd_amount,' \
              ' first_time,' \
              ' last_time,' \
              ' open_times,' \
              ' strth,' \
              ' `limit`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        count = 0
        err = 0
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockLimitDownStocksByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['name'],
                                   val['close'],
                                   val['pct_chg'],
                                   val['amp'],
                                   val['fc_ratio'],
                                   val['fl_ratio'],
                                   val['fd_amount'],
                                   val['first_time'],
                                   val['last_time'],
                                   val['open_times'],
                                   val['strth'],
                                   val['limit']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getAllStockLimitDownStocksByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertCompanyManagersToDatabase(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_company_managers (ts_code,' \
              ' ann_date,' \
              ' name,' \
              ' gender,' \
              ' lev,' \
              ' title,' \
              ' edu,' \
              ' national,' \
              ' birthday,' \
              ' begin_date,' \
              ' end_date,' \
              ' resume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            df = self.getCompanyManagers(stock_code)
            if df is not None:
                for key, val in df.iterrows():
                    values = [[val['ts_code'],
                               val['ann_date'],
                               val['name'],
                               val['gender'],
                               val['lev'],
                               val['title'],
                               val['edu'],
                               val['national'],
                               val['birthday'],
                               val['begin_date'],
                               val['end_date'],
                               val['resume']]]
                    ret = self.dbconn.insertMany(sql, values)
                    if ret == len(values):
                        self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                        count += ret
                    else:
                        self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                        err += len(values)
            else:
                self.logger.error('[getCompanyManagers] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertAllExchangesTradeCalendarToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_exchange_trade_cal (exchange,' \
              ' cal_date,' \
              ' is_open,' \
              ' pretrade_date) VALUES (%s, %s, %s, %s)'
        values = []
        df = self.getAllStockTradeCalendarByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['exchange'],
                               val['cal_date'],
                               val['is_open'],
                               val['pretrade_date']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockTradeCalendarByDate] -> get None')

    def insertStocksProfitToDatabaseByTscode(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_profit (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, basic_eps, ' \
              'diluted_eps, total_revenue, revenue, int_income, prem_earned, comm_income, n_commis_income, ' \
              'n_oth_income, n_oth_b_income, prem_income, out_prem, une_prem_reser, reins_income, n_sec_tb_income, ' \
              'n_sec_uw_income, n_asset_mg_income, oth_b_income, fv_value_chg_gain, invest_income, ass_invest_income, ' \
              'forex_gain, total_cogs, oper_cost, int_exp, comm_exp, biz_tax_surchg, sell_exp, admin_exp, fin_exp, ' \
              'assets_impair_loss, prem_refund, compens_payout, reser_insur_liab, div_payt, reins_exp, oper_exp, ' \
              'compens_payout_refu, insur_reser_refu, reins_cost_refund, other_bus_cost, operate_profit, ' \
              'non_oper_income, non_oper_exp, nca_disploss, total_profit, income_tax, n_income, n_income_attr_p, ' \
              'minority_gain, oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s, ebit, ebitda, ' \
              'insurance_exp, undist_profit, distable_profit, update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockProfitByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['ann_date'],
                                   val['f_ann_date'],
                                   val['end_date'],
                                   val['report_type'],
                                   val['comp_type'],
                                   val['basic_eps'],
                                   val['diluted_eps'],
                                   val['total_revenue'],
                                   val['revenue'],
                                   val['int_income'],
                                   val['prem_earned'],
                                   val['comm_income'],
                                   val['n_commis_income'],
                                   val['n_oth_income'],
                                   val['n_oth_b_income'],
                                   val['prem_income'],
                                   val['out_prem'],
                                   val['une_prem_reser'],
                                   val['reins_income'],
                                   val['n_sec_tb_income'],
                                   val['n_sec_uw_income'],
                                   val['n_asset_mg_income'],
                                   val['oth_b_income'],
                                   val['fv_value_chg_gain'],
                                   val['invest_income'],
                                   val['ass_invest_income'],
                                   val['forex_gain'],
                                   val['total_cogs'],
                                   val['oper_cost'],
                                   val['int_exp'],
                                   val['comm_exp'],
                                   val['biz_tax_surchg'],
                                   val['sell_exp'],
                                   val['admin_exp'],
                                   val['fin_exp'],
                                   val['assets_impair_loss'],
                                   val['prem_refund'],
                                   val['compens_payout'],
                                   val['reser_insur_liab'],
                                   val['div_payt'],
                                   val['reins_exp'],
                                   val['oper_exp'],
                                   val['compens_payout_refu'],
                                   val['insur_reser_refu'],
                                   val['reins_cost_refund'],
                                   val['other_bus_cost'],
                                   val['operate_profit'],
                                   val['non_oper_income'],
                                   val['non_oper_exp'],
                                   val['nca_disploss'],
                                   val['total_profit'],
                                   val['income_tax'],
                                   val['n_income'],
                                   val['n_income_attr_p'],
                                   val['minority_gain'],
                                   val['oth_compr_income'],
                                   val['t_compr_income'],
                                   val['compr_inc_attr_p'],
                                   val['compr_inc_attr_m_s'],
                                   val['ebit'],
                                   val['ebitda'],
                                   val['insurance_exp'],
                                   val['undist_profit'],
                                   val['distable_profit'],
                                   val['update_flag']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockProfitByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksProfitToDatabaseVip(self):
        sql = 'INSERT INTO t_profit (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, basic_eps, ' \
              'diluted_eps, total_revenue, revenue, int_income, prem_earned, comm_income, n_commis_income, ' \
              'n_oth_income, n_oth_b_income, prem_income, out_prem, une_prem_reser, reins_income, n_sec_tb_income, ' \
              'n_sec_uw_income, n_asset_mg_income, oth_b_income, fv_value_chg_gain, invest_income, ass_invest_income, ' \
              'forex_gain, total_cogs, oper_cost, int_exp, comm_exp, biz_tax_surchg, sell_exp, admin_exp, fin_exp, ' \
              'assets_impair_loss, prem_refund, compens_payout, reser_insur_liab, div_payt, reins_exp, oper_exp, ' \
              'compens_payout_refu, insur_reser_refu, reins_cost_refund, other_bus_cost, operate_profit, ' \
              'non_oper_income, non_oper_exp, nca_disploss, total_profit, income_tax, n_income, n_income_attr_p, ' \
              'minority_gain, oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s, ebit, ebitda, ' \
              'insurance_exp, undist_profit, distable_profit, update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockProfitByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['ann_date'],
                               val['f_ann_date'],
                               val['end_date'],
                               val['report_type'],
                               val['comp_type'],
                               val['basic_eps'],
                               val['diluted_eps'],
                               val['total_revenue'],
                               val['revenue'],
                               val['int_income'],
                               val['prem_earned'],
                               val['comm_income'],
                               val['n_commis_income'],
                               val['n_oth_income'],
                               val['n_oth_b_income'],
                               val['prem_income'],
                               val['out_prem'],
                               val['une_prem_reser'],
                               val['reins_income'],
                               val['n_sec_tb_income'],
                               val['n_sec_uw_income'],
                               val['n_asset_mg_income'],
                               val['oth_b_income'],
                               val['fv_value_chg_gain'],
                               val['invest_income'],
                               val['ass_invest_income'],
                               val['forex_gain'],
                               val['total_cogs'],
                               val['oper_cost'],
                               val['int_exp'],
                               val['comm_exp'],
                               val['biz_tax_surchg'],
                               val['sell_exp'],
                               val['admin_exp'],
                               val['fin_exp'],
                               val['assets_impair_loss'],
                               val['prem_refund'],
                               val['compens_payout'],
                               val['reser_insur_liab'],
                               val['div_payt'],
                               val['reins_exp'],
                               val['oper_exp'],
                               val['compens_payout_refu'],
                               val['insur_reser_refu'],
                               val['reins_cost_refund'],
                               val['other_bus_cost'],
                               val['operate_profit'],
                               val['non_oper_income'],
                               val['non_oper_exp'],
                               val['nca_disploss'],
                               val['total_profit'],
                               val['income_tax'],
                               val['n_income'],
                               val['n_income_attr_p'],
                               val['minority_gain'],
                               val['oth_compr_income'],
                               val['t_compr_income'],
                               val['compr_inc_attr_p'],
                               val['compr_inc_attr_m_s'],
                               val['ebit'],
                               val['ebitda'],
                               val['insurance_exp'],
                               val['undist_profit'],
                               val['distable_profit'],
                               val['update_flag']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockProfitByDate] -> get None')

    def insertStocksBalanceSheetToDatabaseByTscode(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_balance_sheet (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, ' \
              'total_share, cap_rese, undistr_porfit, surplus_rese, special_rese, money_cap, trad_asset, ' \
              'notes_receiv, accounts_receiv, oth_receiv, prepayment, div_receiv, int_receiv, inventories, amor_exp, ' \
              'nca_within_1y, sett_rsrv, loanto_oth_bank_fi, premium_receiv, reinsur_receiv, reinsur_res_receiv, ' \
              'pur_resale_fa, oth_cur_assets, total_cur_assets, fa_avail_for_sale, htm_invest, lt_eqt_invest, ' \
              'invest_real_estate, time_deposits, oth_assets, lt_rec, fix_assets, cip, const_materials, ' \
              'fixed_assets_disp, produc_bio_assets, oil_and_gas_assets, intan_assets, r_and_d, goodwill, ' \
              'lt_amor_exp, defer_tax_assets, decr_in_disbur, oth_nca, total_nca, cash_reser_cb, depos_in_oth_bfi, ' \
              'prec_metals, deriv_assets, rr_reins_une_prem, rr_reins_outstd_cla, rr_reins_lins_liab, ' \
              'rr_reins_lthins_liab, refund_depos, ph_pledge_loans, refund_cap_depos, indep_acct_assets, ' \
              'client_depos, client_prov, transac_seat_fee, invest_as_receiv, total_assets, lt_borr, st_borr, ' \
              'cb_borr, depos_ib_deposits, loan_oth_bank, trading_fl, notes_payable, acct_payable, adv_receipts, ' \
              'sold_for_repur_fa, comm_payable, payroll_payable, taxes_payable, int_payable, div_payable, ' \
              'oth_payable, acc_exp, deferred_inc, st_bonds_payable, payable_to_reinsurer, rsrv_insur_cont, ' \
              'acting_trading_sec, acting_uw_sec, non_cur_liab_due_1y, oth_cur_liab, total_cur_liab, bond_payable, ' \
              'lt_payable, specific_payables, estimated_liab, defer_tax_liab, defer_inc_non_cur_liab, oth_ncl, ' \
              'total_ncl, depos_oth_bfi, deriv_liab, depos, agency_bus_liab, oth_liab, prem_receiv_adva, ' \
              'depos_received, ph_invest, reser_une_prem, reser_outstd_claims, reser_lins_liab, reser_lthins_liab, ' \
              'indept_acc_liab, pledge_borr, indem_payable, policy_div_payable, total_liab, treasury_share, ' \
              'ordin_risk_reser, forex_differ, invest_loss_unconf, minority_int, total_hldr_eqy_exc_min_int, ' \
              'total_hldr_eqy_inc_min_int, total_liab_hldr_eqy, lt_payroll_payable, oth_comp_income, oth_eqt_tools, ' \
              'oth_eqt_tools_p_shr, lending_funds, acc_receivable, st_fin_payable, payables, hfs_assets, hfs_sales, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockBalanceSheetByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['ann_date'],
                                   val['f_ann_date'],
                                   val['end_date'],
                                   val['report_type'],
                                   val['comp_type'],
                                   val['total_share'],
                                   val['cap_rese'],
                                   val['undistr_porfit'],
                                   val['surplus_rese'],
                                   val['special_rese'],
                                   val['money_cap'],
                                   val['trad_asset'],
                                   val['notes_receiv'],
                                   val['accounts_receiv'],
                                   val['oth_receiv'],
                                   val['prepayment'],
                                   val['div_receiv'],
                                   val['int_receiv'],
                                   val['inventories'],
                                   val['amor_exp'],
                                   val['nca_within_1y'],
                                   val['sett_rsrv'],
                                   val['loanto_oth_bank_fi'],
                                   val['premium_receiv'],
                                   val['reinsur_receiv'],
                                   val['reinsur_res_receiv'],
                                   val['pur_resale_fa'],
                                   val['oth_cur_assets'],
                                   val['total_cur_assets'],
                                   val['fa_avail_for_sale'],
                                   val['htm_invest'],
                                   val['lt_eqt_invest'],
                                   val['invest_real_estate'],
                                   val['time_deposits'],
                                   val['oth_assets'],
                                   val['lt_rec'],
                                   val['fix_assets'],
                                   val['cip'],
                                   val['const_materials'],
                                   val['fixed_assets_disp'],
                                   val['produc_bio_assets'],
                                   val['oil_and_gas_assets'],
                                   val['intan_assets'],
                                   val['r_and_d'],
                                   val['goodwill'],
                                   val['lt_amor_exp'],
                                   val['defer_tax_assets'],
                                   val['decr_in_disbur'],
                                   val['oth_nca'],
                                   val['total_nca'],
                                   val['cash_reser_cb'],
                                   val['depos_in_oth_bfi'],
                                   val['prec_metals'],
                                   val['deriv_assets'],
                                   val['rr_reins_une_prem'],
                                   val['rr_reins_outstd_cla'],
                                   val['rr_reins_lins_liab'],
                                   val['rr_reins_lthins_liab'],
                                   val['refund_depos'],
                                   val['ph_pledge_loans'],
                                   val['refund_cap_depos'],
                                   val['indep_acct_assets'],
                                   val['client_depos'],
                                   val['client_prov'],
                                   val['transac_seat_fee'],
                                   val['invest_as_receiv'],
                                   val['total_assets'],
                                   val['lt_borr'],
                                   val['st_borr'],
                                   val['cb_borr'],
                                   val['depos_ib_deposits'],
                                   val['loan_oth_bank'],
                                   val['trading_fl'],
                                   val['notes_payable'],
                                   val['acct_payable'],
                                   val['adv_receipts'],
                                   val['sold_for_repur_fa'],
                                   val['comm_payable'],
                                   val['payroll_payable'],
                                   val['taxes_payable'],
                                   val['int_payable'],
                                   val['div_payable'],
                                   val['oth_payable'],
                                   val['acc_exp'],
                                   val['deferred_inc'],
                                   val['st_bonds_payable'],
                                   val['payable_to_reinsurer'],
                                   val['rsrv_insur_cont'],
                                   val['acting_trading_sec'],
                                   val['acting_uw_sec'],
                                   val['non_cur_liab_due_1y'],
                                   val['oth_cur_liab'],
                                   val['total_cur_liab'],
                                   val['bond_payable'],
                                   val['lt_payable'],
                                   val['specific_payables'],
                                   val['estimated_liab'],
                                   val['defer_tax_liab'],
                                   val['defer_inc_non_cur_liab'],
                                   val['oth_ncl'],
                                   val['total_ncl'],
                                   val['depos_oth_bfi'],
                                   val['deriv_liab'],
                                   val['depos'],
                                   val['agency_bus_liab'],
                                   val['oth_liab'],
                                   val['prem_receiv_adva'],
                                   val['depos_received'],
                                   val['ph_invest'],
                                   val['reser_une_prem'],
                                   val['reser_outstd_claims'],
                                   val['reser_lins_liab'],
                                   val['reser_lthins_liab'],
                                   val['indept_acc_liab'],
                                   val['pledge_borr'],
                                   val['indem_payable'],
                                   val['policy_div_payable'],
                                   val['total_liab'],
                                   val['treasury_share'],
                                   val['ordin_risk_reser'],
                                   val['forex_differ'],
                                   val['invest_loss_unconf'],
                                   val['minority_int'],
                                   val['total_hldr_eqy_exc_min_int'],
                                   val['total_hldr_eqy_inc_min_int'],
                                   val['total_liab_hldr_eqy'],
                                   val['lt_payroll_payable'],
                                   val['oth_comp_income'],
                                   val['oth_eqt_tools'],
                                   val['oth_eqt_tools_p_shr'],
                                   val['lending_funds'],
                                   val['acc_receivable'],
                                   val['st_fin_payable'],
                                   val['payables'],
                                   val['hfs_assets'],
                                   val['hfs_sales'],
                                   val['update_flag']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockBalanceSheetByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksBalanceSheetToDatabaseVip(self):
        sql = 'INSERT INTO t_balance_sheet (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, ' \
              'total_share, cap_rese, undistr_porfit, surplus_rese, special_rese, money_cap, trad_asset, ' \
              'notes_receiv, accounts_receiv, oth_receiv, prepayment, div_receiv, int_receiv, inventories, amor_exp, ' \
              'nca_within_1y, sett_rsrv, loanto_oth_bank_fi, premium_receiv, reinsur_receiv, reinsur_res_receiv, ' \
              'pur_resale_fa, oth_cur_assets, total_cur_assets, fa_avail_for_sale, htm_invest, lt_eqt_invest, ' \
              'invest_real_estate, time_deposits, oth_assets, lt_rec, fix_assets, cip, const_materials, ' \
              'fixed_assets_disp, produc_bio_assets, oil_and_gas_assets, intan_assets, r_and_d, goodwill, ' \
              'lt_amor_exp, defer_tax_assets, decr_in_disbur, oth_nca, total_nca, cash_reser_cb, depos_in_oth_bfi, ' \
              'prec_metals, deriv_assets, rr_reins_une_prem, rr_reins_outstd_cla, rr_reins_lins_liab, ' \
              'rr_reins_lthins_liab, refund_depos, ph_pledge_loans, refund_cap_depos, indep_acct_assets, ' \
              'client_depos, client_prov, transac_seat_fee, invest_as_receiv, total_assets, lt_borr, st_borr, ' \
              'cb_borr, depos_ib_deposits, loan_oth_bank, trading_fl, notes_payable, acct_payable, adv_receipts, ' \
              'sold_for_repur_fa, comm_payable, payroll_payable, taxes_payable, int_payable, div_payable, ' \
              'oth_payable, acc_exp, deferred_inc, st_bonds_payable, payable_to_reinsurer, rsrv_insur_cont, ' \
              'acting_trading_sec, acting_uw_sec, non_cur_liab_due_1y, oth_cur_liab, total_cur_liab, bond_payable, ' \
              'lt_payable, specific_payables, estimated_liab, defer_tax_liab, defer_inc_non_cur_liab, oth_ncl, ' \
              'total_ncl, depos_oth_bfi, deriv_liab, depos, agency_bus_liab, oth_liab, prem_receiv_adva, ' \
              'depos_received, ph_invest, reser_une_prem, reser_outstd_claims, reser_lins_liab, reser_lthins_liab, ' \
              'indept_acc_liab, pledge_borr, indem_payable, policy_div_payable, total_liab, treasury_share, ' \
              'ordin_risk_reser, forex_differ, invest_loss_unconf, minority_int, total_hldr_eqy_exc_min_int, ' \
              'total_hldr_eqy_inc_min_int, total_liab_hldr_eqy, lt_payroll_payable, oth_comp_income, oth_eqt_tools, ' \
              'oth_eqt_tools_p_shr, lending_funds, acc_receivable, st_fin_payable, payables, hfs_assets, hfs_sales, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllStockBalanceSheetByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['ann_date'],
                               val['f_ann_date'],
                               val['end_date'],
                               val['report_type'],
                               val['comp_type'],
                               val['total_share'],
                               val['cap_rese'],
                               val['undistr_porfit'],
                               val['surplus_rese'],
                               val['special_rese'],
                               val['money_cap'],
                               val['trad_asset'],
                               val['notes_receiv'],
                               val['accounts_receiv'],
                               val['oth_receiv'],
                               val['prepayment'],
                               val['div_receiv'],
                               val['int_receiv'],
                               val['inventories'],
                               val['amor_exp'],
                               val['nca_within_1y'],
                               val['sett_rsrv'],
                               val['loanto_oth_bank_fi'],
                               val['premium_receiv'],
                               val['reinsur_receiv'],
                               val['reinsur_res_receiv'],
                               val['pur_resale_fa'],
                               val['oth_cur_assets'],
                               val['total_cur_assets'],
                               val['fa_avail_for_sale'],
                               val['htm_invest'],
                               val['lt_eqt_invest'],
                               val['invest_real_estate'],
                               val['time_deposits'],
                               val['oth_assets'],
                               val['lt_rec'],
                               val['fix_assets'],
                               val['cip'],
                               val['const_materials'],
                               val['fixed_assets_disp'],
                               val['produc_bio_assets'],
                               val['oil_and_gas_assets'],
                               val['intan_assets'],
                               val['r_and_d'],
                               val['goodwill'],
                               val['lt_amor_exp'],
                               val['defer_tax_assets'],
                               val['decr_in_disbur'],
                               val['oth_nca'],
                               val['total_nca'],
                               val['cash_reser_cb'],
                               val['depos_in_oth_bfi'],
                               val['prec_metals'],
                               val['deriv_assets'],
                               val['rr_reins_une_prem'],
                               val['rr_reins_outstd_cla'],
                               val['rr_reins_lins_liab'],
                               val['rr_reins_lthins_liab'],
                               val['refund_depos'],
                               val['ph_pledge_loans'],
                               val['refund_cap_depos'],
                               val['indep_acct_assets'],
                               val['client_depos'],
                               val['client_prov'],
                               val['transac_seat_fee'],
                               val['invest_as_receiv'],
                               val['total_assets'],
                               val['lt_borr'],
                               val['st_borr'],
                               val['cb_borr'],
                               val['depos_ib_deposits'],
                               val['loan_oth_bank'],
                               val['trading_fl'],
                               val['notes_payable'],
                               val['acct_payable'],
                               val['adv_receipts'],
                               val['sold_for_repur_fa'],
                               val['comm_payable'],
                               val['payroll_payable'],
                               val['taxes_payable'],
                               val['int_payable'],
                               val['div_payable'],
                               val['oth_payable'],
                               val['acc_exp'],
                               val['deferred_inc'],
                               val['st_bonds_payable'],
                               val['payable_to_reinsurer'],
                               val['rsrv_insur_cont'],
                               val['acting_trading_sec'],
                               val['acting_uw_sec'],
                               val['non_cur_liab_due_1y'],
                               val['oth_cur_liab'],
                               val['total_cur_liab'],
                               val['bond_payable'],
                               val['lt_payable'],
                               val['specific_payables'],
                               val['estimated_liab'],
                               val['defer_tax_liab'],
                               val['defer_inc_non_cur_liab'],
                               val['oth_ncl'],
                               val['total_ncl'],
                               val['depos_oth_bfi'],
                               val['deriv_liab'],
                               val['depos'],
                               val['agency_bus_liab'],
                               val['oth_liab'],
                               val['prem_receiv_adva'],
                               val['depos_received'],
                               val['ph_invest'],
                               val['reser_une_prem'],
                               val['reser_outstd_claims'],
                               val['reser_lins_liab'],
                               val['reser_lthins_liab'],
                               val['indept_acc_liab'],
                               val['pledge_borr'],
                               val['indem_payable'],
                               val['policy_div_payable'],
                               val['total_liab'],
                               val['treasury_share'],
                               val['ordin_risk_reser'],
                               val['forex_differ'],
                               val['invest_loss_unconf'],
                               val['minority_int'],
                               val['total_hldr_eqy_exc_min_int'],
                               val['total_hldr_eqy_inc_min_int'],
                               val['total_liab_hldr_eqy'],
                               val['lt_payroll_payable'],
                               val['oth_comp_income'],
                               val['oth_eqt_tools'],
                               val['oth_eqt_tools_p_shr'],
                               val['lending_funds'],
                               val['acc_receivable'],
                               val['st_fin_payable'],
                               val['payables'],
                               val['hfs_assets'],
                               val['hfs_sales'],
                               val['update_flag']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockBalanceSheetByDate] -> get None')

    def insertStocksCashFlowToDatabaseByTscode(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_cash_flow (ts_code, ann_date, f_ann_date, end_date, comp_type, report_type, net_profit, ' \
              'finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, n_incr_loans_cb, n_inc_borr_oth_fi, ' \
              'prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, n_incr_disp_tfa, ifc_cash_incr, ' \
              'n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur, c_fr_oth_operate_a, c_inf_fr_operate_a, ' \
              'c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, n_incr_clt_loan_adv, n_incr_dep_cbob, ' \
              'c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, oth_cash_pay_oper_act, ' \
              'st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, c_recp_return_invest, ' \
              'n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, c_paid_invest, ' \
              'n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, n_cashflow_inv_act, ' \
              'c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, free_cashflow, ' \
              'c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, ' \
              'stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, ' \
              'c_cash_equ_beg_period, c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, ' \
              'uncon_invest_loss, prov_depr_assets, depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, ' \
              'decr_deferred_exp, incr_acc_exp, loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, ' \
              'decr_def_inc_tax_assets, incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, ' \
              'incr_oper_payable, others, im_net_cashflow_oper_act, conv_debt_into_cap, conv_copbonds_due_within_1y, ' \
              'fa_fnc_leases, end_bal_cash, beg_bal_cash, end_bal_cash_equ, beg_bal_cash_equ, im_n_incr_cash_equ, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockCashflowByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['ann_date'],
                                   val['f_ann_date'],
                                   val['end_date'],
                                   val['comp_type'],
                                   val['report_type'],
                                   val['net_profit'],
                                   val['finan_exp'],
                                   val['c_fr_sale_sg'],
                                   val['recp_tax_rends'],
                                   val['n_depos_incr_fi'],
                                   val['n_incr_loans_cb'],
                                   val['n_inc_borr_oth_fi'],
                                   val['prem_fr_orig_contr'],
                                   val['n_incr_insured_dep'],
                                   val['n_reinsur_prem'],
                                   val['n_incr_disp_tfa'],
                                   val['ifc_cash_incr'],
                                   val['n_incr_disp_faas'],
                                   val['n_incr_loans_oth_bank'],
                                   val['n_cap_incr_repur'],
                                   val['c_fr_oth_operate_a'],
                                   val['c_inf_fr_operate_a'],
                                   val['c_paid_goods_s'],
                                   val['c_paid_to_for_empl'],
                                   val['c_paid_for_taxes'],
                                   val['n_incr_clt_loan_adv'],
                                   val['n_incr_dep_cbob'],
                                   val['c_pay_claims_orig_inco'],
                                   val['pay_handling_chrg'],
                                   val['pay_comm_insur_plcy'],
                                   val['oth_cash_pay_oper_act'],
                                   val['st_cash_out_act'],
                                   val['n_cashflow_act'],
                                   val['oth_recp_ral_inv_act'],
                                   val['c_disp_withdrwl_invest'],
                                   val['c_recp_return_invest'],
                                   val['n_recp_disp_fiolta'],
                                   val['n_recp_disp_sobu'],
                                   val['stot_inflows_inv_act'],
                                   val['c_pay_acq_const_fiolta'],
                                   val['c_paid_invest'],
                                   val['n_disp_subs_oth_biz'],
                                   val['oth_pay_ral_inv_act'],
                                   val['n_incr_pledge_loan'],
                                   val['stot_out_inv_act'],
                                   val['n_cashflow_inv_act'],
                                   val['c_recp_borrow'],
                                   val['proc_issue_bonds'],
                                   val['oth_cash_recp_ral_fnc_act'],
                                   val['stot_cash_in_fnc_act'],
                                   val['free_cashflow'],
                                   val['c_prepay_amt_borr'],
                                   val['c_pay_dist_dpcp_int_exp'],
                                   val['incl_dvd_profit_paid_sc_ms'],
                                   val['oth_cashpay_ral_fnc_act'],
                                   val['stot_cashout_fnc_act'],
                                   val['n_cash_flows_fnc_act'],
                                   val['eff_fx_flu_cash'],
                                   val['n_incr_cash_cash_equ'],
                                   val['c_cash_equ_beg_period'],
                                   val['c_cash_equ_end_period'],
                                   val['c_recp_cap_contrib'],
                                   val['incl_cash_rec_saims'],
                                   val['uncon_invest_loss'],
                                   val['prov_depr_assets'],
                                   val['depr_fa_coga_dpba'],
                                   val['amort_intang_assets'],
                                   val['lt_amort_deferred_exp'],
                                   val['decr_deferred_exp'],
                                   val['incr_acc_exp'],
                                   val['loss_disp_fiolta'],
                                   val['loss_scr_fa'],
                                   val['loss_fv_chg'],
                                   val['invest_loss'],
                                   val['decr_def_inc_tax_assets'],
                                   val['incr_def_inc_tax_liab'],
                                   val['decr_inventories'],
                                   val['decr_oper_payable'],
                                   val['incr_oper_payable'],
                                   val['others'],
                                   val['im_net_cashflow_oper_act'],
                                   val['conv_debt_into_cap'],
                                   val['conv_copbonds_due_within_1y'],
                                   val['fa_fnc_leases'],
                                   val['end_bal_cash'],
                                   val['beg_bal_cash'],
                                   val['end_bal_cash_equ'],
                                   val['beg_bal_cash_equ'],
                                   val['im_n_incr_cash_equ'],
                                   val['update_flag']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockCashflowByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksCashFlowToDatabaseVip(self):
        sql = 'INSERT INTO t_cash_flow (ts_code, ann_date, f_ann_date, end_date, comp_type, report_type, net_profit, ' \
              'finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, n_incr_loans_cb, n_inc_borr_oth_fi, ' \
              'prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, n_incr_disp_tfa, ifc_cash_incr, ' \
              'n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur, c_fr_oth_operate_a, c_inf_fr_operate_a, ' \
              'c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, n_incr_clt_loan_adv, n_incr_dep_cbob, ' \
              'c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, oth_cash_pay_oper_act, ' \
              'st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, c_recp_return_invest, ' \
              'n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, c_paid_invest, ' \
              'n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, n_cashflow_inv_act, ' \
              'c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, free_cashflow, ' \
              'c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, ' \
              'stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, ' \
              'c_cash_equ_beg_period, c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, ' \
              'uncon_invest_loss, prov_depr_assets, depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, ' \
              'decr_deferred_exp, incr_acc_exp, loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, ' \
              'decr_def_inc_tax_assets, incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, ' \
              'incr_oper_payable, others, im_net_cashflow_oper_act, conv_debt_into_cap, conv_copbonds_due_within_1y, ' \
              'fa_fnc_leases, end_bal_cash, beg_bal_cash, end_bal_cash_equ, beg_bal_cash_equ, im_n_incr_cash_equ, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getAllStockCashflowByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['ann_date'],
                               val['f_ann_date'],
                               val['end_date'],
                               val['comp_type'],
                               val['report_type'],
                               val['net_profit'],
                               val['finan_exp'],
                               val['c_fr_sale_sg'],
                               val['recp_tax_rends'],
                               val['n_depos_incr_fi'],
                               val['n_incr_loans_cb'],
                               val['n_inc_borr_oth_fi'],
                               val['prem_fr_orig_contr'],
                               val['n_incr_insured_dep'],
                               val['n_reinsur_prem'],
                               val['n_incr_disp_tfa'],
                               val['ifc_cash_incr'],
                               val['n_incr_disp_faas'],
                               val['n_incr_loans_oth_bank'],
                               val['n_cap_incr_repur'],
                               val['c_fr_oth_operate_a'],
                               val['c_inf_fr_operate_a'],
                               val['c_paid_goods_s'],
                               val['c_paid_to_for_empl'],
                               val['c_paid_for_taxes'],
                               val['n_incr_clt_loan_adv'],
                               val['n_incr_dep_cbob'],
                               val['c_pay_claims_orig_inco'],
                               val['pay_handling_chrg'],
                               val['pay_comm_insur_plcy'],
                               val['oth_cash_pay_oper_act'],
                               val['st_cash_out_act'],
                               val['n_cashflow_act'],
                               val['oth_recp_ral_inv_act'],
                               val['c_disp_withdrwl_invest'],
                               val['c_recp_return_invest'],
                               val['n_recp_disp_fiolta'],
                               val['n_recp_disp_sobu'],
                               val['stot_inflows_inv_act'],
                               val['c_pay_acq_const_fiolta'],
                               val['c_paid_invest'],
                               val['n_disp_subs_oth_biz'],
                               val['oth_pay_ral_inv_act'],
                               val['n_incr_pledge_loan'],
                               val['stot_out_inv_act'],
                               val['n_cashflow_inv_act'],
                               val['c_recp_borrow'],
                               val['proc_issue_bonds'],
                               val['oth_cash_recp_ral_fnc_act'],
                               val['stot_cash_in_fnc_act'],
                               val['free_cashflow'],
                               val['c_prepay_amt_borr'],
                               val['c_pay_dist_dpcp_int_exp'],
                               val['incl_dvd_profit_paid_sc_ms'],
                               val['oth_cashpay_ral_fnc_act'],
                               val['stot_cashout_fnc_act'],
                               val['n_cash_flows_fnc_act'],
                               val['eff_fx_flu_cash'],
                               val['n_incr_cash_cash_equ'],
                               val['c_cash_equ_beg_period'],
                               val['c_cash_equ_end_period'],
                               val['c_recp_cap_contrib'],
                               val['incl_cash_rec_saims'],
                               val['uncon_invest_loss'],
                               val['prov_depr_assets'],
                               val['depr_fa_coga_dpba'],
                               val['amort_intang_assets'],
                               val['lt_amort_deferred_exp'],
                               val['decr_deferred_exp'],
                               val['incr_acc_exp'],
                               val['loss_disp_fiolta'],
                               val['loss_scr_fa'],
                               val['loss_fv_chg'],
                               val['invest_loss'],
                               val['decr_def_inc_tax_assets'],
                               val['incr_def_inc_tax_liab'],
                               val['decr_inventories'],
                               val['decr_oper_payable'],
                               val['incr_oper_payable'],
                               val['others'],
                               val['im_net_cashflow_oper_act'],
                               val['conv_debt_into_cap'],
                               val['conv_copbonds_due_within_1y'],
                               val['fa_fnc_leases'],
                               val['end_bal_cash'],
                               val['beg_bal_cash'],
                               val['end_bal_cash_equ'],
                               val['beg_bal_cash_equ'],
                               val['im_n_incr_cash_equ'],
                               val['update_flag']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockCashflowByDate] -> get None')

    def insertStocksExpressNewsToDatabaseByTscode(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_express_news (ts_code, ann_date, end_date, revenue, operate_profit, total_profit, ' \
              'n_income, total_assets, total_hldr_eqy_exc_min_int, diluted_eps, diluted_roe, yoy_net_profit, bps, ' \
              'yoy_sales, yoy_op, yoy_tp, yoy_dedu_np, yoy_eps, yoy_roe, growth_assets, yoy_equity, growth_bps, ' \
              'or_last_year, op_last_year, tp_last_year, np_last_year, eps_last_year, open_net_assets, open_bps, ' \
              'perf_summary, is_audit, remark) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockExpressNewsByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['ann_date'],
                                   val['end_date'],
                                   val['revenue'],
                                   val['operate_profit'],
                                   val['total_profit'],
                                   val['n_income'],
                                   val['total_assets'],
                                   val['total_hldr_eqy_exc_min_int'],
                                   val['diluted_eps'],
                                   val['diluted_roe'],
                                   val['yoy_net_profit'],
                                   val['bps'],
                                   val['yoy_sales'],
                                   val['yoy_op'],
                                   val['yoy_tp'],
                                   val['yoy_dedu_np'],
                                   val['yoy_eps'],
                                   val['yoy_roe'],
                                   val['growth_assets'],
                                   val['yoy_equity'],
                                   val['growth_bps'],
                                   val['or_last_year'],
                                   val['op_last_year'],
                                   val['tp_last_year'],
                                   val['np_last_year'],
                                   val['eps_last_year'],
                                   val['open_net_assets'],
                                   val['open_bps'],
                                   val['perf_summary'],
                                   val['is_audit'],
                                   val['remark']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockExpressNewsByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksExpressNewsToDatabaseVip(self):
        sql = 'INSERT INTO t_express_news (ts_code, ann_date, end_date, revenue, operate_profit, total_profit, ' \
              'n_income, total_assets, total_hldr_eqy_exc_min_int, diluted_eps, diluted_roe, yoy_net_profit, bps, ' \
              'yoy_sales, yoy_op, yoy_tp, yoy_dedu_np, yoy_eps, yoy_roe, growth_assets, yoy_equity, growth_bps, ' \
              'or_last_year, op_last_year, tp_last_year, np_last_year, eps_last_year, open_net_assets, open_bps, ' \
              'perf_summary, is_audit, remark) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getAllStockExpressNewsByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['ann_date'],
                               val['end_date'],
                               val['revenue'],
                               val['operate_profit'],
                               val['total_profit'],
                               val['n_income'],
                               val['total_assets'],
                               val['total_hldr_eqy_exc_min_int'],
                               val['diluted_eps'],
                               val['diluted_roe'],
                               val['yoy_net_profit'],
                               val['bps'],
                               val['yoy_sales'],
                               val['yoy_op'],
                               val['yoy_tp'],
                               val['yoy_dedu_np'],
                               val['yoy_eps'],
                               val['yoy_roe'],
                               val['growth_assets'],
                               val['yoy_equity'],
                               val['growth_bps'],
                               val['or_last_year'],
                               val['op_last_year'],
                               val['tp_last_year'],
                               val['np_last_year'],
                               val['eps_last_year'],
                               val['open_net_assets'],
                               val['open_bps'],
                               val['perf_summary'],
                               val['is_audit'],
                               val['remark']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockExpressNewsByDate] -> get None')

    def insertStocksFinanceIndicatorToDatabaseByTscode(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_finance_indicator (ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, ' \
              'revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps, extra_item, profit_dedt, gross_margin, ' \
              'current_ratio, quick_ratio, cash_ratio, invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, ' \
              'fa_turn, assets_turn, op_income, valuechange_income, interst_income, daa, ebit, ebitda, fcff, fcfe, ' \
              'current_exint, noncurrent_exint, interestdebt, netdebt, tangible_asset, working_capital, ' \
              'networking_capital, invest_capital, retained_earnings, diluted2_eps, bps, ocfps, retainedps, cfps, ' \
              'ebit_ps, fcff_ps, fcfe_ps, netprofit_margin, grossprofit_margin, cogs_of_sales, expense_of_sales, ' \
              'profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, gc_of_gr, op_of_gr, ebit_of_gr, ' \
              'roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, opincome_of_ebt, ' \
              'investincome_of_ebt, n_op_profit_of_ebt, tax_to_ebt, dtprofit_to_profit, salescash_to_or, ocf_to_or, ' \
              'ocf_to_opincome, capitalized_to_da, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, ca_to_assets, ' \
              'nca_to_assets, tbassets_to_totalassets, int_to_talcap, eqt_to_talcapital, currentdebt_to_debt, ' \
              'longdeb_to_debt, ocf_to_shortdebt, debt_to_eqt, eqt_to_debt, eqt_to_interestdebt, ' \
              'tangibleasset_to_debt, tangasset_to_intdebt, tangibleasset_to_netdebt, ocf_to_debt, ' \
              'ocf_to_interestdebt, ocf_to_netdebt, ebit_to_interest, longdebt_to_workingcapital, ebitda_to_debt, ' \
              'turn_days, roa_yearly, roa_dp, fixed_assets, profit_prefin_exp, non_op_profit, op_to_ebt, nop_to_ebt, ' \
              'ocf_to_profit, cash_to_liqdebt, cash_to_liqdebt_withinterest, op_to_liqdebt, op_to_debt, roic_yearly, ' \
              'total_fa_trun, profit_to_op, q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, ' \
              'q_gsprofit_margin, q_exp_to_sales, q_profit_to_gr, q_saleexp_to_gr, q_adminexp_to_gr, q_finaexp_to_gr, ' \
              'q_impair_to_gr_ttm, q_gc_to_gr, q_op_to_gr, q_roe, q_dt_roe, q_npta, q_opincome_to_ebt, ' \
              'q_investincome_to_ebt, q_dtprofit_to_profit, q_salescash_to_or, q_ocf_to_sales, q_ocf_to_or, ' \
              'basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy, ' \
              'roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, q_gr_yoy, q_gr_qoq, q_sales_yoy, q_sales_qoq, ' \
              'q_op_yoy, q_op_qoq, q_profit_yoy, q_profit_qoq, q_netprofit_yoy, q_netprofit_qoq, equity_yoy, rd_exp, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockFinanceIndicatorByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['ann_date'],
                                   val['end_date'],
                                   val['eps'],
                                   val['dt_eps'],
                                   val['total_revenue_ps'],
                                   val['revenue_ps'],
                                   val['capital_rese_ps'],
                                   val['surplus_rese_ps'],
                                   val['undist_profit_ps'],
                                   val['extra_item'],
                                   val['profit_dedt'],
                                   val['gross_margin'],
                                   val['current_ratio'],
                                   val['quick_ratio'],
                                   val['cash_ratio'],
                                   val['invturn_days'],
                                   val['arturn_days'],
                                   val['inv_turn'],
                                   val['ar_turn'],
                                   val['ca_turn'],
                                   val['fa_turn'],
                                   val['assets_turn'],
                                   val['op_income'],
                                   val['valuechange_income'],
                                   val['interst_income'],
                                   val['daa'],
                                   val['ebit'],
                                   val['ebitda'],
                                   val['fcff'],
                                   val['fcfe'],
                                   val['current_exint'],
                                   val['noncurrent_exint'],
                                   val['interestdebt'],
                                   val['netdebt'],
                                   val['tangible_asset'],
                                   val['working_capital'],
                                   val['networking_capital'],
                                   val['invest_capital'],
                                   val['retained_earnings'],
                                   val['diluted2_eps'],
                                   val['bps'],
                                   val['ocfps'],
                                   val['retainedps'],
                                   val['cfps'],
                                   val['ebit_ps'],
                                   val['fcff_ps'],
                                   val['fcfe_ps'],
                                   val['netprofit_margin'],
                                   val['grossprofit_margin'],
                                   val['cogs_of_sales'],
                                   val['expense_of_sales'],
                                   val['profit_to_gr'],
                                   val['saleexp_to_gr'],
                                   val['adminexp_of_gr'],
                                   val['finaexp_of_gr'],
                                   val['impai_ttm'],
                                   val['gc_of_gr'],
                                   val['op_of_gr'],
                                   val['ebit_of_gr'],
                                   val['roe'],
                                   val['roe_waa'],
                                   val['roe_dt'],
                                   val['roa'],
                                   val['npta'],
                                   val['roic'],
                                   val['roe_yearly'],
                                   val['roa2_yearly'],
                                   val['roe_avg'],
                                   val['opincome_of_ebt'],
                                   val['investincome_of_ebt'],
                                   val['n_op_profit_of_ebt'],
                                   val['tax_to_ebt'],
                                   val['dtprofit_to_profit'],
                                   val['salescash_to_or'],
                                   val['ocf_to_or'],
                                   val['ocf_to_opincome'],
                                   val['capitalized_to_da'],
                                   val['debt_to_assets'],
                                   val['assets_to_eqt'],
                                   val['dp_assets_to_eqt'],
                                   val['ca_to_assets'],
                                   val['nca_to_assets'],
                                   val['tbassets_to_totalassets'],
                                   val['int_to_talcap'],
                                   val['eqt_to_talcapital'],
                                   val['currentdebt_to_debt'],
                                   val['longdeb_to_debt'],
                                   val['ocf_to_shortdebt'],
                                   val['debt_to_eqt'],
                                   val['eqt_to_debt'],
                                   val['eqt_to_interestdebt'],
                                   val['tangibleasset_to_debt'],
                                   val['tangasset_to_intdebt'],
                                   val['tangibleasset_to_netdebt'],
                                   val['ocf_to_debt'],
                                   val['ocf_to_interestdebt'],
                                   val['ocf_to_netdebt'],
                                   val['ebit_to_interest'],
                                   val['longdebt_to_workingcapital'],
                                   val['ebitda_to_debt'],
                                   val['turn_days'],
                                   val['roa_yearly'],
                                   val['roa_dp'],
                                   val['fixed_assets'],
                                   val['profit_prefin_exp'],
                                   val['non_op_profit'],
                                   val['op_to_ebt'],
                                   val['nop_to_ebt'],
                                   val['ocf_to_profit'],
                                   val['cash_to_liqdebt'],
                                   val['cash_to_liqdebt_withinterest'],
                                   val['op_to_liqdebt'],
                                   val['op_to_debt'],
                                   val['roic_yearly'],
                                   val['total_fa_trun'],
                                   val['profit_to_op'],
                                   val['q_opincome'],
                                   val['q_investincome'],
                                   val['q_dtprofit'],
                                   val['q_eps'],
                                   val['q_netprofit_margin'],
                                   val['q_gsprofit_margin'],
                                   val['q_exp_to_sales'],
                                   val['q_profit_to_gr'],
                                   val['q_saleexp_to_gr'],
                                   val['q_adminexp_to_gr'],
                                   val['q_finaexp_to_gr'],
                                   val['q_impair_to_gr_ttm'],
                                   val['q_gc_to_gr'],
                                   val['q_op_to_gr'],
                                   val['q_roe'],
                                   val['q_dt_roe'],
                                   val['q_npta'],
                                   val['q_opincome_to_ebt'],
                                   val['q_investincome_to_ebt'],
                                   val['q_dtprofit_to_profit'],
                                   val['q_salescash_to_or'],
                                   val['q_ocf_to_sales'],
                                   val['q_ocf_to_or'],
                                   val['basic_eps_yoy'],
                                   val['dt_eps_yoy'],
                                   val['cfps_yoy'],
                                   val['op_yoy'],
                                   val['ebt_yoy'],
                                   val['netprofit_yoy'],
                                   val['dt_netprofit_yoy'],
                                   val['ocf_yoy'],
                                   val['roe_yoy'],
                                   val['bps_yoy'],
                                   val['assets_yoy'],
                                   val['eqt_yoy'],
                                   val['tr_yoy'],
                                   val['or_yoy'],
                                   val['q_gr_yoy'],
                                   val['q_gr_qoq'],
                                   val['q_sales_yoy'],
                                   val['q_sales_qoq'],
                                   val['q_op_yoy'],
                                   val['q_op_qoq'],
                                   val['q_profit_yoy'],
                                   val['q_profit_qoq'],
                                   val['q_netprofit_yoy'],
                                   val['q_netprofit_qoq'],
                                   val['equity_yoy'],
                                   val['rd_exp'],
                                   val['update_flag']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockFinanceIndicatorByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksFinanceIndicatorToDatabaseVip(self):
        sql = 'INSERT INTO t_finance_indicator (ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, ' \
              'revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps, extra_item, profit_dedt, gross_margin, ' \
              'current_ratio, quick_ratio, cash_ratio, invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, ' \
              'fa_turn, assets_turn, op_income, valuechange_income, interst_income, daa, ebit, ebitda, fcff, fcfe, ' \
              'current_exint, noncurrent_exint, interestdebt, netdebt, tangible_asset, working_capital, ' \
              'networking_capital, invest_capital, retained_earnings, diluted2_eps, bps, ocfps, retainedps, cfps, ' \
              'ebit_ps, fcff_ps, fcfe_ps, netprofit_margin, grossprofit_margin, cogs_of_sales, expense_of_sales, ' \
              'profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, gc_of_gr, op_of_gr, ebit_of_gr, ' \
              'roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, opincome_of_ebt, ' \
              'investincome_of_ebt, n_op_profit_of_ebt, tax_to_ebt, dtprofit_to_profit, salescash_to_or, ocf_to_or, ' \
              'ocf_to_opincome, capitalized_to_da, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, ca_to_assets, ' \
              'nca_to_assets, tbassets_to_totalassets, int_to_talcap, eqt_to_talcapital, currentdebt_to_debt, ' \
              'longdeb_to_debt, ocf_to_shortdebt, debt_to_eqt, eqt_to_debt, eqt_to_interestdebt, ' \
              'tangibleasset_to_debt, tangasset_to_intdebt, tangibleasset_to_netdebt, ocf_to_debt, ' \
              'ocf_to_interestdebt, ocf_to_netdebt, ebit_to_interest, longdebt_to_workingcapital, ebitda_to_debt, ' \
              'turn_days, roa_yearly, roa_dp, fixed_assets, profit_prefin_exp, non_op_profit, op_to_ebt, nop_to_ebt, ' \
              'ocf_to_profit, cash_to_liqdebt, cash_to_liqdebt_withinterest, op_to_liqdebt, op_to_debt, roic_yearly, ' \
              'total_fa_trun, profit_to_op, q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, ' \
              'q_gsprofit_margin, q_exp_to_sales, q_profit_to_gr, q_saleexp_to_gr, q_adminexp_to_gr, q_finaexp_to_gr, ' \
              'q_impair_to_gr_ttm, q_gc_to_gr, q_op_to_gr, q_roe, q_dt_roe, q_npta, q_opincome_to_ebt, ' \
              'q_investincome_to_ebt, q_dtprofit_to_profit, q_salescash_to_or, q_ocf_to_sales, q_ocf_to_or, ' \
              'basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy, ' \
              'roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, q_gr_yoy, q_gr_qoq, q_sales_yoy, q_sales_qoq, ' \
              'q_op_yoy, q_op_qoq, q_profit_yoy, q_profit_qoq, q_netprofit_yoy, q_netprofit_qoq, equity_yoy, rd_exp, ' \
              'update_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getAllStockFinanceIndicatorByDate(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['ann_date'],
                               val['end_date'],
                               val['eps'],
                               val['dt_eps'],
                               val['total_revenue_ps'],
                               val['revenue_ps'],
                               val['capital_rese_ps'],
                               val['surplus_rese_ps'],
                               val['undist_profit_ps'],
                               val['extra_item'],
                               val['profit_dedt'],
                               val['gross_margin'],
                               val['current_ratio'],
                               val['quick_ratio'],
                               val['cash_ratio'],
                               val['invturn_days'],
                               val['arturn_days'],
                               val['inv_turn'],
                               val['ar_turn'],
                               val['ca_turn'],
                               val['fa_turn'],
                               val['assets_turn'],
                               val['op_income'],
                               val['valuechange_income'],
                               val['interst_income'],
                               val['daa'],
                               val['ebit'],
                               val['ebitda'],
                               val['fcff'],
                               val['fcfe'],
                               val['current_exint'],
                               val['noncurrent_exint'],
                               val['interestdebt'],
                               val['netdebt'],
                               val['tangible_asset'],
                               val['working_capital'],
                               val['networking_capital'],
                               val['invest_capital'],
                               val['retained_earnings'],
                               val['diluted2_eps'],
                               val['bps'],
                               val['ocfps'],
                               val['retainedps'],
                               val['cfps'],
                               val['ebit_ps'],
                               val['fcff_ps'],
                               val['fcfe_ps'],
                               val['netprofit_margin'],
                               val['grossprofit_margin'],
                               val['cogs_of_sales'],
                               val['expense_of_sales'],
                               val['profit_to_gr'],
                               val['saleexp_to_gr'],
                               val['adminexp_of_gr'],
                               val['finaexp_of_gr'],
                               val['impai_ttm'],
                               val['gc_of_gr'],
                               val['op_of_gr'],
                               val['ebit_of_gr'],
                               val['roe'],
                               val['roe_waa'],
                               val['roe_dt'],
                               val['roa'],
                               val['npta'],
                               val['roic'],
                               val['roe_yearly'],
                               val['roa2_yearly'],
                               val['roe_avg'],
                               val['opincome_of_ebt'],
                               val['investincome_of_ebt'],
                               val['n_op_profit_of_ebt'],
                               val['tax_to_ebt'],
                               val['dtprofit_to_profit'],
                               val['salescash_to_or'],
                               val['ocf_to_or'],
                               val['ocf_to_opincome'],
                               val['capitalized_to_da'],
                               val['debt_to_assets'],
                               val['assets_to_eqt'],
                               val['dp_assets_to_eqt'],
                               val['ca_to_assets'],
                               val['nca_to_assets'],
                               val['tbassets_to_totalassets'],
                               val['int_to_talcap'],
                               val['eqt_to_talcapital'],
                               val['currentdebt_to_debt'],
                               val['longdeb_to_debt'],
                               val['ocf_to_shortdebt'],
                               val['debt_to_eqt'],
                               val['eqt_to_debt'],
                               val['eqt_to_interestdebt'],
                               val['tangibleasset_to_debt'],
                               val['tangasset_to_intdebt'],
                               val['tangibleasset_to_netdebt'],
                               val['ocf_to_debt'],
                               val['ocf_to_interestdebt'],
                               val['ocf_to_netdebt'],
                               val['ebit_to_interest'],
                               val['longdebt_to_workingcapital'],
                               val['ebitda_to_debt'],
                               val['turn_days'],
                               val['roa_yearly'],
                               val['roa_dp'],
                               val['fixed_assets'],
                               val['profit_prefin_exp'],
                               val['non_op_profit'],
                               val['op_to_ebt'],
                               val['nop_to_ebt'],
                               val['ocf_to_profit'],
                               val['cash_to_liqdebt'],
                               val['cash_to_liqdebt_withinterest'],
                               val['op_to_liqdebt'],
                               val['op_to_debt'],
                               val['roic_yearly'],
                               val['total_fa_trun'],
                               val['profit_to_op'],
                               val['q_opincome'],
                               val['q_investincome'],
                               val['q_dtprofit'],
                               val['q_eps'],
                               val['q_netprofit_margin'],
                               val['q_gsprofit_margin'],
                               val['q_exp_to_sales'],
                               val['q_profit_to_gr'],
                               val['q_saleexp_to_gr'],
                               val['q_adminexp_to_gr'],
                               val['q_finaexp_to_gr'],
                               val['q_impair_to_gr_ttm'],
                               val['q_gc_to_gr'],
                               val['q_op_to_gr'],
                               val['q_roe'],
                               val['q_dt_roe'],
                               val['q_npta'],
                               val['q_opincome_to_ebt'],
                               val['q_investincome_to_ebt'],
                               val['q_dtprofit_to_profit'],
                               val['q_salescash_to_or'],
                               val['q_ocf_to_sales'],
                               val['q_ocf_to_or'],
                               val['basic_eps_yoy'],
                               val['dt_eps_yoy'],
                               val['cfps_yoy'],
                               val['op_yoy'],
                               val['ebt_yoy'],
                               val['netprofit_yoy'],
                               val['dt_netprofit_yoy'],
                               val['ocf_yoy'],
                               val['roe_yoy'],
                               val['bps_yoy'],
                               val['assets_yoy'],
                               val['eqt_yoy'],
                               val['tr_yoy'],
                               val['or_yoy'],
                               val['q_gr_yoy'],
                               val['q_gr_qoq'],
                               val['q_sales_yoy'],
                               val['q_sales_qoq'],
                               val['q_op_yoy'],
                               val['q_op_qoq'],
                               val['q_profit_yoy'],
                               val['q_profit_qoq'],
                               val['q_netprofit_yoy'],
                               val['q_netprofit_qoq'],
                               val['equity_yoy'],
                               val['rd_exp'],
                               val['update_flag']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockFinanceIndicatorByDate] -> get None')

    def insertTopListToDatabaseByDate(self):
        sql = 'INSERT INTO t_toplist (ts_code, trade_date, name, close, pct_change, turnover_rate, amount, l_sell, ' \
              'l_buy, l_amount, net_amount, net_rate, amount_rate, float_values, reason) VALUES (%s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getTopList(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['name'],
                               val['close'],
                               val['pct_change'],
                               val['turnover_rate'],
                               val['amount'],
                               val['l_sell'],
                               val['l_buy'],
                               val['l_amount'],
                               val['net_amount'],
                               val['net_rate'],
                               val['amount_rate'],
                               val['float_values'],
                               val['reason']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getTopList] -> get None')

    def insertTopListTradeDetailToDatabaseByDate(self):
        sql = 'INSERT INTO t_toplist_trade_detail (ts_code, trade_date, exalter, buy, buy_rate, sell, sell_rate, ' \
              'net_buy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getTopListTradeDetail(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['exalter'],
                               val['buy'],
                               val['buy_rate'],
                               val['sell'],
                               val['sell_rate'],
                               val['net_buy']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getTopListTradeDetail] -> get None')

    def insertConceptToDatabase(self):
        sql = 'INSERT INTO t_concept (code, name, src) VALUES (%s, %s, %s)'
        values = []
        df = self.getConcept()
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['code'],
                               val['name'],
                               val['src']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getConcept] -> get None')

    def insertStocksConceptToDatabase(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_stocks_concept (ts_code, code, concept_name, name, in_date, out_date) VALUES (%s, %s, ' \
              '%s, %s, %s, %s) '
        for stock_code in self.stock_list:
            values = []
            df = self.getConceptByStock(stock_code)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['id'],
                                   val['concept_name'],
                                   val['name'],
                                   val['in_date'],
                                   val['out_date']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getConceptByStock] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertBigTradeDetailToDatabaseByDate(self):
        sql = 'INSERT INTO t_big_trade (ts_code, trade_date, price, vol, amount, buyer, seller) VALUES (%s, %s, %s, ' \
              '%s, %s, %s, %s) '
        values = []
        df = self.getAllStockBigTradeDetailByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['price'],
                               val['vol'],
                               val['amount'],
                               val['buyer'],
                               val['seller']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockBigTradeDetailByDate] -> get None')

    def insertBigTradeDetailToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_big_trade (ts_code, trade_date, price, vol, amount, buyer, seller) VALUES (%s, %s, %s, ' \
              '%s, %s, %s, %s) '
        count = 0
        err = 0
        for stock_code in self.stock_list:
            values = []
            df = self.getSignalStockBigTradeDetailByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['price'],
                                   val['vol'],
                                   val['amount'],
                                   val['buyer'],
                                   val['seller']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalStockBigTradeDetailByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexBaseInformationToDatabase(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_index_base (ts_code, name, fullname, market, publisher, index_type, category, base_date, ' \
              'base_point, list_date, weight_rule, `desc`, exp_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s) '
        for m in self.market:
            df = self.getIndexBasicInformation(m)
            if df is not None:
                for key, val in df.iterrows():
                    values = [[val['ts_code'],
                               val['name'],
                               val['fullname'],
                               val['market'],
                               val['publisher'],
                               val['index_type'],
                               val['category'],
                               val['base_date'],
                               val['base_point'],
                               val['list_date'],
                               val['weight_rule'],
                               val['desc'],
                               val['exp_date']]]
                    ret = self.dbconn.insertMany(sql, values)
                    if ret == len(values):
                        self.logger.debug('%s insert %d datas to database' % (m, ret))
                        count += ret
                    else:
                        self.logger.error('%s insert data to database get some error: %d' % (m, ret))
                        err += len(values)
            else:
                self.logger.error('[getIndexBasicInformation] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexDailyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_index_daily (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for index_code in self.index_list:
            values = []
            df = self.getSignalIndexDailyQuantByDate(index_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s all insert %d datas' % (index_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (index_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalIndexDailyQuantByDate] -> %s get None' % index_code)

        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexDailyQuantToDatabaseByDate(self):
        sql = 'INSERT INTO t_index_daily (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllIndexDailyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('all insert %d datas' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.warning('[getAllIndexDailyQuantByDate] -> get None')

    def insertIndexWeeklyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_index_weekly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for index_code in self.index_list:
            values = []
            df = self.getSignalIndexWeeklyQuantByDate(index_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s all insert %d datas' % (index_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (index_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalIndexWeeklyQuantByDate] -> %s get None' % index_code)

        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexWeeklyQuantToDatabaseByDate(self):
        sql = 'INSERT INTO t_index_weekly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllIndexWeeklyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('all insert %d datas' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.warning('[getAllIndexWeeklyQuantByDate] -> get None')

    def insertIndexMonthlyQuantToDatabaseByDateRange(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_index_monthly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for index_code in self.index_list:
            values = []
            df = self.getSignalIndexMonthlyQuantByDate(index_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['open'],
                                   val['high'],
                                   val['low'],
                                   val['close'],
                                   val['pre_close'],
                                   val['change'],
                                   val['pct_chg'],
                                   val['vol'],
                                   val['amount']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s all insert %d datas' % (index_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert to database get some error: %d' % (index_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalIndexMonthlyQuantByDate] -> %s get None' % index_code)

        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexMonthlyQuantToDatabaseByDate(self):
        sql = 'INSERT INTO t_index_monthly (ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, ' \
              'pct_chg, vol, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getAllIndexMonthlyQuantByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['open'],
                               val['high'],
                               val['low'],
                               val['close'],
                               val['pre_close'],
                               val['change'],
                               val['pct_chg'],
                               val['vol'],
                               val['amount']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.debug('all insert %d datas' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.warning('[getAllIndexMonthlyQuantByDate] -> get None')

    def insertIndexIndicatorToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_index_indicator (ts_code, trade_date, total_mv, float_mv, total_share, float_share, ' \
              'free_share, turnover_rate, turnover_rate_f, pe, pe_ttm, pb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s)'
        count = 0
        err = 0
        for stock_code in self.index_list:
            values = []
            df = self.getSignalIndexDailyIndicatorByDate(stock_code, self.start_date, self.end_date)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
                                   val['trade_date'],
                                   val['total_mv'],
                                   val['float_mv'],
                                   val['total_share'],
                                   val['float_share'],
                                   val['free_share'],
                                   val['turnover_rate'],
                                   val['turnover_rate_f'],
                                   val['pe'],
                                   val['pe_ttm'],
                                   val['pb']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getSignalIndexDailyIndicatorByDate] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertIndexIndicatorToDatabaseByDate(self):
        sql = 'INSERT INTO t_index_indicator (ts_code, trade_date, total_mv, float_mv, total_share, float_share, ' \
              'free_share, turnover_rate, turnover_rate_f, pe, pe_ttm, pb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s)'
        values = []
        df = self.getAllIndexDailyIndicatorByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
                               val['trade_date'],
                               val['total_mv'],
                               val['float_mv'],
                               val['total_share'],
                               val['float_share'],
                               val['free_share'],
                               val['turnover_rate'],
                               val['turnover_rate_f'],
                               val['pe'],
                               val['pe_ttm'],
                               val['pb']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllIndexDailyIndicatorByDate] -> get None')

    def insertSWClassifyToDatabase(self):
        count = 0
        err = 0
        sql = 'INSERT INTO t_sw_classify (index_code, industry_name, level, industry_code, src) VALUES (%s, %s, %s, ' \
              '%s, %s) '
        for l in ['L1', 'L2', 'L3']:
            values = []
            df = self.getSWClassify(l)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['index_code'],
                                   val['industry_name'],
                                   val['level'],
                                   val['industry_code'],
                                   val['src']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (l, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (l, ret))
                    err += len(values)
            else:
                self.logger.error('[getSWClassify] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertStocksSWClassifyToDatabase(self):
        sql = 'INSERT INTO t_stocks_sw_classify (ts_code, index_code, index_name, con_name, in_date, out_date, ' \
              'is_new) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        count = 0
        err = 0
        for stock_code in self.stock_list:
            values = []
            df = self.getStockSWIndustry(stock_code)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['con_code'],
                                   val['index_code'],
                                   val['index_name'],
                                   val['con_name'],
                                   val['in_date'],
                                   val['out_date'],
                                   val['is_new']])
                ret = self.dbconn.insertMany(sql, values)
                if ret == len(values):
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += len(values)
            else:
                self.logger.error('[getStockSWIndustry] -> get None')
        self.logger.info('all insert %d datas to database and %d errors' % (count, err))

    def insertDailySummaryToDatabaseByDate(self):
        sql = 'INSERT INTO t_daily_summary (trade_date, ts_code, ts_name, com_count, total_share, float_share, ' \
              'total_mv, float_mv, amount, vol, trans_count, pe, tr, exchange) VALUES (%s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getTradeSummaryByDate(self.trade_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['trade_date'],
                               val['ts_code'],
                               val['ts_name'],
                               val['com_count'],
                               val['total_share'],
                               val['float_share'],
                               val['total_mv'],
                               val['float_mv'],
                               val['amount'],
                               val['vol'],
                               val['trans_count'],
                               val['pe'],
                               val['tr'],
                               val['exchange']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getTradeSummaryByDate] -> get None')

    def insertDailySummaryToDatabaseByDateRange(self):
        sql = 'INSERT INTO t_daily_summary (trade_date, ts_code, ts_name, com_count, total_share, float_share, ' \
              'total_mv, float_mv, amount, vol, trans_count, pe, tr, exchange) VALUES (%s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s) '
        values = []
        df = self.getTradeSummaryByDateRange(self.start_date, self.end_date)
        if df is not None:
            for key, val in df.iterrows():
                values.append([val['trade_date'],
                               val['ts_code'],
                               val['ts_name'],
                               val['com_count'],
                               val['total_share'],
                               val['float_share'],
                               val['total_mv'],
                               val['float_mv'],
                               val['amount'],
                               val['vol'],
                               val['trans_count'],
                               val['pe'],
                               val['tr'],
                               val['exchange']])
            ret = self.dbconn.insertMany(sql, values)
            if ret == len(values):
                self.logger.info('all insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getTradeSummaryByDateRange] -> get None')

    def methods(self):
        return list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)), dir(self)))


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--daily_quotation', type=bool,
                        help='Get daily quotation from tushare, default: False', default=False)
    parser.add_argument('--weekly_quotation', type=bool,
                        help='Get weekly quotation from tushare, default: False', default=False)
    parser.add_argument('--monthly_quotation', type=bool,
                        help='Get monthly quotation from tushare, default: False', default=False)
    parser.add_argument('--qfq_daily_quotation', type=bool,
                        help='Get qfq daily quotation from tushare, default: False', default=False)
    parser.add_argument('--hfq_daily_quotation', type=bool,
                        help='Get hfq daily quotation from tushare, default: False', default=False)
    parser.add_argument('--qfq_weekly_quotation', type=bool,
                        help='Get qfq weekly quotation from tushare, default: False', default=False)
    parser.add_argument('--hfq_weekly_quotation', type=bool,
                        help='Get hfq weekly quotation from tushare, default: False', default=False)
    parser.add_argument('--qfq_monthly_quotation', type=bool,
                        help='Get qfq monthly quotation from tushare, default: False', default=False)
    parser.add_argument('--hfq_monthly_quotation', type=bool,
                        help='Get hfq monthly quotation from tushare, default: False', default=False)
    parser.add_argument('--daily_index', type=bool,
                        help='Get daily index from tushare, default: False', default=False)
    parser.add_argument('--flash_news', type=bool,
                        help='Get flash news from tushare, default: False', default=False)
    parser.add_argument('--major_news', type=bool,
                        help='Get major news from tushare, default: False', default=False)
    parser.add_argument('--adj_factor', type=bool,
                        help='Get adjust factor, default: False', default=False)
    parser.add_argument('--index_base', type=bool,
                        help='index base information, default: False', default=False)
    parser.add_argument('--limit_up', type=bool,
                        help='limit up stocks, default: False', default=False)
    parser.add_argument('--limit_down', type=bool,
                        help='limit down stocks, default: False', default=False)
    parser.add_argument('--limit_price', type=bool,
                        help='stocks limit price, default: False', default=False)
    parser.add_argument('--money_flow', type=bool,
                        help='stocks money flow, default: False', default=False)
    parser.add_argument('--company_base', type=bool,
                        help='company base information, default: False', default=False)
    parser.add_argument('--company_managers', type=bool,
                        help='company managers information, default: False', default=False)
    parser.add_argument('--trader_cal', type=bool,
                        help='trader calendar information, default: False', default=False)
    parser.add_argument('--profit', type=bool,
                        help='stocks profit, default: False', default=False)
    parser.add_argument('--balance_sheet', type=bool,
                        help='stocks balance sheet, default: False', default=False)
    parser.add_argument('--cash_flow', type=bool,
                        help='stocks cash flow, default: False', default=False)
    parser.add_argument('--exp_news', type=bool,
                        help='stocks express news, default: False', default=False)
    parser.add_argument('--fin_indicator', type=bool,
                        help='stocks finance indicator, default: False', default=False)
    parser.add_argument('--top_list', type=bool,
                        help='top list stocks, default: False', default=False)
    parser.add_argument('--top_list_detail', type=bool,
                        help='top list trader details, default: False', default=False)
    parser.add_argument('--concept', type=bool,
                        help='concept, default: False', default=False)
    parser.add_argument('--concept_stocks', type=bool,
                        help='concept stocks, default: False', default=False)
    parser.add_argument('--big_trade', type=bool,
                        help='big trade details, default: False', default=False)
    parser.add_argument('--index_daily', type=bool,
                        help='index daily quants, default: False', default=False)
    parser.add_argument('--index_weekly', type=bool,
                        help='index weekly quants, default: False', default=False)
    parser.add_argument('--index_monthly', type=bool,
                        help='index monthly quants, default: False', default=False)
    parser.add_argument('--index_daily_ind', type=bool,
                        help='index daily indicator, default: False', default=False)
    parser.add_argument('--sw_class', type=bool,
                        help='sw L1,L2,L3 classify, default: False', default=False)
    parser.add_argument('--sw_class_stock', type=bool,
                        help='stocks sw classify, default: False', default=False)
    parser.add_argument('--trade_sum', type=bool,
                        help='trade summary by exchange, default: False', default=False)
    parser.add_argument('--logdir', type=str,
                        help='Log directory, default: /opt/quantification/logs', default='.\\logs\\')
    parser.add_argument('--loglevel', type=str,
                        help='Log level, default: info', default='info')
    parser.add_argument('--startdate', type=str,
                        help='Start date, default: today', default='')
    parser.add_argument('--enddate', type=str,
                        help='End date, default: today', default='')
    parser.add_argument('--trade_date', type=str,
                        help='trade date, default: today', default='')
    parser.add_argument('--retry', type=int,
                        help='Exception retry times, default: 3', default=3)
    parser.add_argument('--intv', type=int,
                        help='interval, default 0.5s', default=0.5)
    return parser.parse_args(argv)


def addTask(t_list, logger, func, args):
    logger.info('开始启动 %s 线程' % func.__name__)
    try:
        tid = threading.Thread(target=func, args=args)
        tid.start()
    except Exception as e:
        logger.error('启动 %s 线程失败: %s' % (func.__name__, e))
    else:
        t_list.append(tid)
        logger.info('线程: %s 启动成功, TID: %s-%d' % (func.__name__, tid.getName(), tid.ident))


def continueLoop(threads):
    for t in threads:
        if t.is_alive():
            return True
    return False


def runForDateRange(args):
    threads_list = []
    s = time.time()
    # 日志
    if not os.path.exists(os.path.expanduser(args.logdir)):
        os.mkdir(os.path.expanduser(args.logdir))
    logger = log.init_logging(os.path.join(os.path.expanduser(args.logdir),
                                           '%s_%s.txt' % (
                                               __name__, time.strftime('%Y%m%d', time.localtime(time.time())))),
                              args.loglevel)

    print('Start: %s-%s-%s' % (args.startdate, args.enddate, args.trade_date))

    # tushare batch api
    api = batchBusiness(start=args.startdate,
                        end=args.enddate,
                        trade_date=args.trade_date,
                        logger=logger,
                        retry=args.retry,
                        intv=args.intv)

    # 线程
    if args.daily_quotation:
        addTask(threads_list, logger, api.insertDailyQuantToDatabaseByDateRange, ())
    if args.weekly_quotation:
        addTask(threads_list, logger, api.insertWeeklyQuantToDatabaseByDateRange, ())
    if args.monthly_quotation:
        addTask(threads_list, logger, api.insertMonthlyQuantToDatabasebyDateRange, ())
    if args.qfq_daily_quotation:
        addTask(threads_list, logger, api.insertQfqDailyQuantToDatabaseByDateRange, ())
    if args.hfq_daily_quotation:
        addTask(threads_list, logger, api.insertHfqDailyQuantToDatabaseByDateRange, ())
    if args.qfq_weekly_quotation:
        addTask(threads_list, logger, api.insertQfqWeeklyQuantToDatabaseByDateRange, ())
    if args.hfq_weekly_quotation:
        addTask(threads_list, logger, api.insertHfqWeeklyQuantToDatabaseByDateRange, ())
    if args.qfq_monthly_quotation:
        addTask(threads_list, logger, api.insertQfqMonthlyQuantToDatabaseByDateRange, ())
    if args.hfq_monthly_quotation:
        addTask(threads_list, logger, api.insertHfqMonthlyQuantToDatabaseByDateRange, ())
    if args.daily_index:
        addTask(threads_list, logger, api.insertDailyIndexToDatabaseByDateRange, ())
    if args.flash_news:
        addTask(threads_list, logger, api.insert24HFlashNewsToDatabase, ())
    if args.major_news:
        addTask(threads_list, logger, api.insertMojorNewsToDatabase, ())
    if args.adj_factor:
        addTask(threads_list, logger, api.insertAdjFactorToDatabaseByDateRange, ())
    if args.index_base:
        addTask(threads_list, logger, api.insertIndexBaseInformationToDatabase, ())
    if args.limit_up:
        addTask(threads_list, logger, api.insertLimitUpStocksToDatabaseByDateRange, ())
    if args.limit_down:
        addTask(threads_list, logger, api.insertLimitDownStocksToDatabaseByDateRange, ())
    if args.limit_price:
        addTask(threads_list, logger, api.insertStocksLimitPriceToDatabaseByDateRange, ())
    if args.money_flow:
        addTask(threads_list, logger, api.insertStocksMoneyFlowToDatabaseByDateRange, ())
    if args.company_base:
        addTask(threads_list, logger, api.insertCompanyBaseInformationToDatabaseByExchange, ())
    if args.company_managers:
        addTask(threads_list, logger, api.insertCompanyManagersToDatabase, ())
    if args.trader_cal:
        addTask(threads_list, logger, api.insertAllExchangesTradeCalendarToDatabaseByDateRange, ())
    if args.profit:
        addTask(threads_list, logger, api.insertStocksProfitToDatabaseByTscode, ())
    if args.balance_sheet:
        addTask(threads_list, logger, api.insertStocksBalanceSheetToDatabaseByTscode, ())
    if args.cash_flow:
        addTask(threads_list, logger, api.insertStocksCashFlowToDatabaseByTscode, ())
    if args.exp_news:
        addTask(threads_list, logger, api.insertStocksExpressNewsToDatabaseByTscode, ())
    if args.fin_indicator:
        addTask(threads_list, logger, api.insertStocksFinanceIndicatorToDatabaseByTscode, ())
    if args.top_list:
        addTask(threads_list, logger, api.insertTopListToDatabaseByDate, ())
    if args.top_list_detail:
        addTask(threads_list, logger, api.insertTopListTradeDetailToDatabaseByDate, ())
    if args.concept:
        addTask(threads_list, logger, api.insertConceptToDatabase, ())
    if args.concept_stocks:
        addTask(threads_list, logger, api.insertStocksConceptToDatabase, ())
    if args.big_trade:
        addTask(threads_list, logger, api.insertBigTradeDetailToDatabaseByDateRange, ())
    if args.index_daily:
        addTask(threads_list, logger, api.insertIndexDailyQuantToDatabaseByDateRange, ())
    if args.index_weekly:
        addTask(threads_list, logger, api.insertIndexWeeklyQuantToDatabaseByDateRange, ())
    if args.index_monthly:
        addTask(threads_list, logger, api.insertIndexMonthlyQuantToDatabaseByDateRange, ())
    if args.index_daily_ind:
        addTask(threads_list, logger, api.insertIndexIndicatorToDatabaseByDateRange, ())
    if args.sw_class:
        addTask(threads_list, logger, api.insertSWClassifyToDatabase, ())
    if args.sw_class_stock:
        addTask(threads_list, logger, api.insertStocksSWClassifyToDatabase, ())
    if args.trade_sum:
        addTask(threads_list, logger, api.insertDailySummaryToDatabaseByDateRange, ())

    while continueLoop(threads_list):
        time.sleep(1)

    logger.info('All complete with [%d] sec' % (time.time() - s))


def runForDate(args):
    threads_list = []
    s = time.time()
    # 日志
    if not os.path.exists(os.path.expanduser(args.logdir)):
        os.mkdir(os.path.expanduser(args.logdir))
    logger = log.init_logging(os.path.join(os.path.expanduser(args.logdir),
                                           '%s_%s.txt' % (
                                               __name__, time.strftime('%Y%m%d', time.localtime(time.time())))),
                              args.loglevel)

    print('Start: %s-%s-%s' % (args.startdate, args.enddate, args.trade_date))

    # tushare batch api
    api = batchBusiness(start=args.startdate,
                        end=args.enddate,
                        trade_date=args.trade_date,
                        logger=logger,
                        retry=args.retry,
                        intv=args.intv)

    # 更新基础数据
    api.insertCompanyBaseInformationToDatabaseByExchange()
    api.insertCompanyManagersToDatabase()
    api.insertStockBaseInformationToDatabase()
    api.insertIndexBaseInformationToDatabase()

    # 线程
    if args.daily_quotation:
        addTask(threads_list, logger, api.insertDailyQuantToDatabaseByDate, ())
    if args.weekly_quotation:
        addTask(threads_list, logger, api.insertWeeklyQuantToDatabaseByDate, ())
    if args.monthly_quotation:
        addTask(threads_list, logger, api.insertMonthlyQuantToDatabaseByDate, ())
    if args.qfq_daily_quotation:
        addTask(threads_list, logger, api.insertQfqDailyQuantToDatabaseByDateRange, ())
    if args.hfq_daily_quotation:
        addTask(threads_list, logger, api.insertHfqDailyQuantToDatabaseByDateRange, ())
    if args.qfq_weekly_quotation:
        addTask(threads_list, logger, api.insertQfqWeeklyQuantToDatabaseByDateRange, ())
    if args.hfq_weekly_quotation:
        addTask(threads_list, logger, api.insertHfqWeeklyQuantToDatabaseByDateRange, ())
    if args.qfq_monthly_quotation:
        addTask(threads_list, logger, api.insertQfqMonthlyQuantToDatabaseByDateRange, ())
    if args.hfq_monthly_quotation:
        addTask(threads_list, logger, api.insertHfqMonthlyQuantToDatabaseByDateRange, ())
    if args.daily_index:
        addTask(threads_list, logger, api.insertDailyIndexToDatabaseByDate, ())
    if args.flash_news:
        addTask(threads_list, logger, api.insert24HFlashNewsToDatabase, ())
    if args.major_news:
        addTask(threads_list, logger, api.insertMojorNewsToDatabase, ())
    if args.adj_factor:
        addTask(threads_list, logger, api.insertAdjFactorToDatabaseByDate, ())
    if args.index_base:
        addTask(threads_list, logger, api.insertIndexBaseInformationToDatabase, ())
    if args.limit_up:
        addTask(threads_list, logger, api.insertLimitUpStocksToDatabaseByDate, ())
    if args.limit_down:
        addTask(threads_list, logger, api.insertLimitDownStocksToDatabaseByDate, ())
    if args.limit_price:
        addTask(threads_list, logger, api.insertStocksLimitPriceToDatabaseByDate, ())
    if args.money_flow:
        addTask(threads_list, logger, api.insertStocksMoneyFlowToDatabaseByDate, ())
    if args.company_base:
        addTask(threads_list, logger, api.insertCompanyBaseInformationToDatabaseByExchange, ())
    if args.company_managers:
        addTask(threads_list, logger, api.insertCompanyManagersToDatabase, ())
    if args.trader_cal:
        addTask(threads_list, logger, api.insertAllExchangesTradeCalendarToDatabaseByDateRange, ())
    if args.profit:
        addTask(threads_list, logger, api.insertStocksProfitToDatabaseByTscode, ())
    if args.balance_sheet:
        addTask(threads_list, logger, api.insertStocksBalanceSheetToDatabaseByTscode, ())
    if args.cash_flow:
        addTask(threads_list, logger, api.insertStocksCashFlowToDatabaseByTscode, ())
    if args.exp_news:
        addTask(threads_list, logger, api.insertStocksExpressNewsToDatabaseByTscode, ())
    if args.fin_indicator:
        addTask(threads_list, logger, api.insertStocksFinanceIndicatorToDatabaseByTscode, ())
    if args.top_list:
        addTask(threads_list, logger, api.insertTopListToDatabaseByDate, ())
    if args.top_list_detail:
        addTask(threads_list, logger, api.insertTopListTradeDetailToDatabaseByDate, ())
    if args.concept:
        addTask(threads_list, logger, api.insertConceptToDatabase, ())
    if args.concept_stocks:
        addTask(threads_list, logger, api.insertStocksConceptToDatabase, ())
    if args.big_trade:
        addTask(threads_list, logger, api.insertBigTradeDetailToDatabaseByDate, ())
    if args.index_daily:
        addTask(threads_list, logger, api.insertIndexDailyQuantToDatabaseByDate, ())
    if args.index_weekly:
        addTask(threads_list, logger, api.insertIndexWeeklyQuantToDatabaseByDate, ())
    if args.index_monthly:
        addTask(threads_list, logger, api.insertIndexMonthlyQuantToDatabaseByDate, ())
    if args.index_daily_ind:
        addTask(threads_list, logger, api.insertIndexIndicatorToDatabaseByDate, ())
    if args.sw_class:
        addTask(threads_list, logger, api.insertSWClassifyToDatabase, ())
    if args.sw_class_stock:
        addTask(threads_list, logger, api.insertStocksSWClassifyToDatabase, ())
    if args.trade_sum:
        addTask(threads_list, logger, api.insertDailySummaryToDatabaseByDate, ())

    while continueLoop(threads_list):
        print('\r<%08d>s [\\], see log to more information' % (time.time() - s), end='')
        time.sleep(0.1)
        print('\r<%08d>s [/], see log to more information' % (time.time() - s), end='')
        time.sleep(0.1)

    logger.info('All complete with [%d] sec' % (time.time() - s))


if __name__ == '__main__':
    # 同步基础数据: --sw_class_stock True --sw_class True --concept True --concept_stocks True --company_base True
    # --company_managers True
    # 同步指数、财务等行情: --limit_price True --limit_up True --limit_down True
    # --money_flow True --trader_cal True --profit True --big_trade True
    # --balance_sheet True --cash_flow True --exp_news True --fin_indicator True --index_daily True --index_weekly
    # True --index_monthly True --index_daily_ind True --startdate 20100101 --enddate 20200414
    # runForDateRange(parse_arguments(sys.argv[1:]))
    # 每日同步: --daily_quotation True --weekly_quotation True --monthly_quotation True --qfq_daily_quotation True
    # --hfq_daily_quotation True --qfq_weekly_quotation True --hfq_weekly_quotation True --qfq_monthly_quotation True
    # --hfq_monthly_quotation True --daily_index True -adj_factor True --index_base True --limit_up True --limit_down
    # True --limit_price True --money_flow True --company_base True --company_managers True --trader_cal True
    # --profit True --balance_sheet True --cash_flow True --exp_news True --fin_indicator True --top_list True
    # --top_list_detail True --concept_stocks True --big_trade True --index_daily True --index_weekly True
    # --index_monthly True --index_daily_ind True --sw_class_stock True --trade_sum True --logdir /opt/ --loglevel
    # info --startdate '' --enddate '' --trade_date '' --retry 5 --intv 0.5
    runForDate(parse_arguments(sys.argv[1:]))
