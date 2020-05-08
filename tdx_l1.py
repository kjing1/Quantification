# python 3.7.4
# coding = utf-8
# filename tdx_l1.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

from db.dbpool import MyPymysqlPool
import log
from tdx.api import tdxApi
from typing import Dict
from enum import Enum
import time
import os
import threading
import time
import sys
import random


class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    CFFEX = "CFFEX"  # China Financial Futures Exchange
    SHFE = "SHFE"  # Shanghai Futures Exchange
    CZCE = "CZCE"  # Zhengzhou Commodity Exchange
    DCE = "DCE"  # Dalian Commodity Exchange
    INE = "INE"  # Shanghai International Energy Exchange
    SSE = "SSE"  # Shanghai Stock Exchange
    SZSE = "SZSE"  # Shenzhen Stock Exchange
    SGE = "SGE"  # Shanghai Gold Exchange
    WXE = "WXE"  # Wuxi Steel Exchange

    # Global
    SMART = "SMART"  # Smart Router for US stocks
    NYMEX = "NYMEX"  # New York Mercantile Exchange
    COMEX = "COMEX"  # a division of theNew York Mercantile Exchange
    GLOBEX = "GLOBEX"  # Globex of CME
    IDEALPRO = "IDEALPRO"  # Forex ECN of Interactive Brokers
    CME = "CME"  # Chicago Mercantile Exchange
    ICE = "ICE"  # Intercontinental Exchange
    SEHK = "SEHK"  # Stock Exchange of Hong Kong
    HKFE = "HKFE"  # Hong Kong Futures Exchange
    HKSE = "HKSE"  # Hong Kong Stock Exchange
    SGX = "SGX"  # Singapore Global Exchange
    CBOT = "CBT"  # Chicago Board of Trade
    CBOE = "CBOE"  # Chicago Board Options Exchange
    CFE = "CFE"  # CBOE Futures Exchange
    DME = "DME"  # Dubai Mercantile Exchange
    EUREX = "EUX"  # Eurex Exchange
    APEX = "APEX"  # Asia Pacific Exchange
    LME = "LME"  # London Metal Exchange
    BMD = "BMD"  # Bursa Malaysia Derivatives
    TOCOM = "TOCOM"  # Tokyo Commodity Exchange
    EUNX = "EUNX"  # Euronext Exchange
    KRX = "KRX"  # Korean Exchange

    OANDA = "OANDA"  # oanda.com

    # CryptoCurrency
    BITMEX = "BITMEX"
    OKEX = "OKEX"
    HUOBI = "HUOBI"
    BITFINEX = "BITFINEX"
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"  # bybit.com
    COINBASE = "COINBASE"
    DERIBIT = "DERIBIT"
    GATEIO = "GATEIO"
    BITSTAMP = "BITSTAMP"

    # Special Function
    LOCAL = "LOCAL"  # For local generated data


EXCAHNGE2TDXMARKET: Dict[Exchange, int] = {
    Exchange.SZSE: 0,
    Exchange.SSE: 1
}

TDXMARKET2EXCHANGE: Dict[int, Exchange] = {v: k for k, v in EXCAHNGE2TDXMARKET.items()}

MAXTHREADS = 32


class tdxL1Business(tdxApi):
    def __init__(self, dbpool=None):
        super().__init__()
        if dbpool is None:
            self.dbconn = MyPymysqlPool(None, 'MysqlDatabaseInfo')
        else:
            self.dbconn = dbpool
        self.stock_list = []
        self.connect()
        self.getStocksList()

    def __del__(self):
        self.release()
        # self.dbconn.dispose()

    def insertTdxL1QuotesToDatabase(self, stock_code_list):
        sql = 'INSERT INTO t_tdx_l1 (market, code, active1, price, last_close, open, high, low, servertime, ' \
              'reversed_bytes0, reversed_bytes1, vol, cur_vol, amount, s_vol, b_vol, reversed_bytes2, ' \
              'reversed_bytes3, bid1, ask1, bid_vol1, ask_vol1, bid2, ask2, bid_vol2, ask_vol2, bid3, ask3, bid_vol3, ' \
              'ask_vol3, bid4, ask4, bid_vol4, ask_vol4, bid5, ask5, bid_vol5, ask_vol5, reversed_bytes4, ' \
              'reversed_bytes5, reversed_bytes6, reversed_bytes7, reversed_bytes8, reversed_bytes9, active2) VALUES (' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        df = self.getQuotes(stock_code_list)
        if df is None:
            self.logger.error('Get None')
            return
        values = []
        for key, val in df.iterrows():
            m = TDXMARKET2EXCHANGE[int(val['market'])].value
            if m == Exchange.SSE.value:
                ts_code = val['code'] + '.SH'
            elif m == Exchange.SZSE.value:
                ts_code = val['code'] + '.SZ'
            else:
                ts_code = val['code']
            values.append([m,
                           ts_code,
                           val['active1'],
                           val['price'],
                           val['last_close'],
                           val['open'],
                           val['high'],
                           val['low'],
                           val['servertime'],
                           val['reversed_bytes0'],
                           val['reversed_bytes1'],
                           val['vol'],
                           val['cur_vol'],
                           val['amount'],
                           val['s_vol'],
                           val['b_vol'],
                           val['reversed_bytes2'],
                           val['reversed_bytes3'],
                           val['bid1'],
                           val['ask1'],
                           val['bid_vol1'],
                           val['ask_vol1'],
                           val['bid2'],
                           val['ask2'],
                           val['bid_vol2'],
                           val['ask_vol2'],
                           val['bid3'],
                           val['ask3'],
                           val['bid_vol3'],
                           val['ask_vol3'],
                           val['bid4'],
                           val['ask4'],
                           val['bid_vol4'],
                           val['ask_vol4'],
                           val['bid5'],
                           val['ask5'],
                           val['bid_vol5'],
                           val['ask_vol5'],
                           val['reversed_bytes4'],
                           val['reversed_bytes5'],
                           val['reversed_bytes6'],
                           val['reversed_bytes7'],
                           val['reversed_bytes8'],
                           val['reversed_bytes9'],
                           val['active2']])
        ret = self.dbconn.insertMany(sql, values)
        if ret == len(values):
            self.logger.info('all insert %d datas to database' % ret)
        else:
            self.logger.info('insert data to database get some error: %d' % ret)

    def getStocksList(self):
        for market in [0, 1]:
            m_count = self.getCount(market)
            index = 0
            while index < m_count:
                for key, val in self.getList(market, index).iterrows():
                    self.stock_list.append((market, val['code']))
                    index += 1


def runGetTdxL1(logger, dbpool, stock_list):
    api = tdxL1Business(dbpool)
    while True:
        s = time.time()
        api.insertTdxL1QuotesToDatabase(stock_list)
        e = time.time()
        logger.info('%d stocks L1 quoets with [%d] sec' % (len(stock_list), e - s))
        if e-s > 60:
            continue
        else:
            time.sleep(60-(e-s))


def init_deamon():
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    # decouple from parent environment
    os.chdir(".")
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            print("Daemon PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        print("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)


def split_list(src_list, size, new_list=[]):
    if len(src_list) < size:
        new_list.append(src_list)
        return new_list
    else:
        new_list.append(src_list[:size])
        return split_list(src_list[size:], size, new_list)


if __name__ == '__main__':
    # init_deamon()
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    logdir_exp = os.path.expanduser('.\\logs\\')
    if not os.path.exists(logdir_exp):
        os.makedirs(logdir_exp)
    logger = log.init_logging(os.path.join(logdir_exp, '%s_%s.txt' % (__name__ + 'tdx', today)), 'info')
    threads_list = []

    start = time.time()
    dbpool = MyPymysqlPool(None, 'MysqlDatabaseInfo')
    ret = dbpool.getAll('select table_name from information_schema.tables where table_schema="quantification" and table_type="base table" and table_name="t_min_qf";')
    print(ret)
    exit()
    dbpool.common_execute('CREATE TABLE `t_min_qfq_000001` (`ts_code` varchar(128) NOT NULL COMMENT "tushare代码",`timestamp` '
                          'varchar(128) NOT NULL COMMENT "交易日期",`open` varchar(128) DEFAULT NULL COMMENT "开盘价",'
                          '`close` varchar(128) DEFAULT NULL,`low` varchar(128) DEFAULT NULL,`high` varchar(128) '
                          'DEFAULT NULL,`volume` varchar(128) DEFAULT NULL,`money` varchar(128) DEFAULT NULL,'
                          '`factor` varchar(128) DEFAULT NULL,`high_limit` varchar(128) DEFAULT NULL,`low_limit` '
                          'varchar(128) DEFAULT NULL,`avg` varchar(128) DEFAULT NULL,`pre_close` varchar(128) DEFAULT '
                          'NULL,`paused` varchar(128) DEFAULT NULL,`open_interest` varchar(128) DEFAULT NULL,'
                          'PRIMARY KEY (`ts_code`,`timestamp`) USING BTREE,KEY `UQ_TS_CODE` (`ts_code`),'
                          'KEY `UQ_TRADE_DATE` (`timestamp`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    exit()

    api = tdxL1Business(dbpool)
    s_list = split_list(api.stock_list, 80)
    all_stocks = len(api.stock_list)
    del api

    for stocks in s_list:
        try:
            t = threading.Thread(target=runGetTdxL1, args=(logger, dbpool, [stocks]))
            t.start()
        except Exception as e:
            logger.error('线程启动失败 [%s-%d] with args:%s' % (t.getName(), t.ident, stocks))
        threads_list.append(t)

    print('All %d threads' % len(threads_list))
    while True:
        print('\r<%08d>s [\\], see log to more information' % (time.time() - start), end='')
        time.sleep(0.1)
        print('\r<%08d>s [/], see log to more information' % (time.time() - start), end='')
        time.sleep(0.1)
