# python 3.7.4
# coding = utf-8
# filename t_daily_t_daily_index_sync.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from tus.api import tusApi, MYTOKEN
from db import dbpool
import os
import log
import time


class batchBusiness(tusApi):
    def __init__(self, start, end, trade_date=''):
        super().__init__(MYTOKEN, retry=5, timeout=30, intv=0.5)
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.logger = log.init_logging(os.path.join(os.path.expanduser('.'), '%s_%s.txt' % (__name__, today)), 'info')
        self.dbconn = dbpool.MyPymysqlPool(self.logger, 'MysqlDatabaseInfo')
        self.stock_list = []
        self.start_date = start
        self.end_date = end
        if trade_date == '':
            self.trade_date = today
        else:
            self.trade_date = trade_date

        self.getAllStockCodeFromDatabase()

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
        values = []
        df = self.getAllStockBaseInformation()
        if df is None:
            self.logger.error('[getAllStockBaseInformation] -> get None, retry')
        else:
            for key, val in df.iterrows():
                values.append([val['ts_code'],
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
                               val['is_hs']])
            ret = self.dbconn.insertMany(sql, values)
            if ret > 0:
                self.logger.info('insert %d data to database' % ret)
            else:
                self.logger.warn('insert to database may be some errors, all insert %d' % ret)

    def getAllStockCodeFromDatabase(self):
        all_fetched = self.dbconn.getAll('SELECT ts_code FROM t_stocks')
        if all_fetched is not None:
            for d in all_fetched:
                self.stock_list.append(d['ts_code'])
        else:
            self.logger.warn('get None')

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
                if ret > 0:
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
            if ret > 0:
                self.logger.debug('all insert %d datas' % ret)
            else:
                self.logger.error('insert to database get some error: %d' % ret)
        else:
            self.logger.warn('[getAllStockDailyQuantByDate] -> get None')

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
                if ret > 0:
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
            if ret > 0:
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
                if ret > 0:
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
            if ret > 0:
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
        sql = 'INSERT INTO s_flash_news (type, source, creat_date, content, pub_datetime) VALUES (' \
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
                if ret > 0:
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
        sql = 'INSERT INTO s_information (title, type, source, creat_date, content, pub_datetime) VALUES (' \
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
            if ret > 0:
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
                if ret > 0:
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
            if ret > 0:
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
            if ret > 0:
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
            values = []
            df = self.getCompanyBaseInformationByExchange(e)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
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
                                   val['business_scope']])
                ret = self.dbconn.insertMany(sql, values)
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (e, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (e, ret))
                    err += ret
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
            if ret > 0:
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
            if ret > 0:
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s inseret data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
            if ret > 0:
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
            if ret > 0:
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
              ' limit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getLimitUpStocksByDate(self.trade_date)
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
            if ret > 0:
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getLimitUpStocksByDate] -> get None')

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
              ' limit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = []
        df = self.getLimitDownStocksByDate(self.trade_date)
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
            if ret > 0:
                self.logger.info('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getLimitDownStocksByDate] -> get None')

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
            values = []
            df = self.getCompanyManagers(stock_code)
            if df is not None:
                for key, val in df.iterrows():
                    values.append([val['ts_code'],
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
                                   val['resume']])
                ret = self.dbconn.insertMany(sql, values)
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
            if ret > 0:
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
            if ret > 0:
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
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
                if ret > 0:
                    self.logger.debug('%s insert %d datas to database' % (stock_code, ret))
                    count += ret
                else:
                    self.logger.error('%s insert data to database get some error: %d' % (stock_code, ret))
                    err += ret
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
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
            if ret > 0:
                self.logger.debug('insert %d datas to database' % ret)
            else:
                self.logger.error('insert data to database get some error: %d' % ret)
        else:
            self.logger.error('[getAllStockBalanceSheetByDate] -> get None')
