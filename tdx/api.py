# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

from pytdx.hq import TdxHq_API
from pytdx.pool.hqpool import TdxHqPool_API
from pytdx.pool.ippool import AvailableIPPool
from pytdx.config.hosts import hq_hosts
import random


class tdxApi:
    def __init__(self):
        self.ipset = [(v[1], v[2]) for v in hq_hosts]
        random.shuffle(self.ipset)
        self.ipset5 = self.ipset[:5]
        self.ippool = AvailableIPPool(TdxHq_API, self.ipset5)
        self.primary_ip, self.hot_backup_ip = self.ippool.sync_get_top_n(2)
        # self.api = TdxHqPool_API(TdxHq_API, self.ippool)
        self.api = TdxHq_API(multithread=True, heartbeat=True, auto_retry=True)

    def connect(self):
        # self.api.connect(self.primary_ip, self.hot_backup_ip)
        self.api.connect(self.primary_ip[0], self.primary_ip[1])

    def release(self):
        self.api.disconnect()

    def getQuotes(self, stock_list):
        # df = self.api1.to_df(self.api.get_security_quotes(stock_list))
        datas = self.api.get_security_quotes(stock_list)
        if datas is None:
            return None
        else:
            return self.api.to_df(datas)

    def getList(self, market, index):
        df = self.api.to_df(self.api.get_security_list(market, index))
        return df

    def getCount(self, market=0):
        return self.api.get_security_count(market)

    def getMinQuotes(self, market, stock_code):
        datas = self.api.get_minute_time_data(market, stock_code)
        if datas is None:
            return None

        return self.api.to_df(datas)

    def getMinQuotesHis(self, market, stock_code, date):
        datas = self.api.get_history_minute_time_data(market, stock_code, date)
        if datas is None:
            return None

        return self.api.to_df(datas)


if __name__ == '__main__':
    test = tdxApi()
    test.connect()
    df = test.getQuotes([(0, '000001')])
    for key, val in df.iterrows():
        print(val)
    exit()
    with open('.\\min.txt', 'w') as f:
        f.write('get min quotes: price - vol\n')
        df = test.getMinQuotes(0, '000001')
        for key, val in df.iterrows():
            f.write('%d - %d\n' % (val['price'], val['vol']))

    with open('.\\min_his.txt', 'w') as f:
        f.write('get min his quotes: price - vol\n')
        for date in ['20200420', '20200421', '20200422']:
            f.write('%s\n' % date)
            df = test.getMinQuotesHis(0, '000001', date)
            for key, val in df.iterrows():
                f.write('%d - %d\n' % (val['price'], val['vol']))
    test.release()
    exit()
    stock_list = []
    for market in [0, 1]:
        m_count = test.getCount(market)
        index = 0
        while index < m_count:
            for key, val in test.getList(market, index).iterrows():
                stock_list.append((market, val['code']))
                index += 1
    print(stock_list)
    exit()
    df = test.getList(0,0)
    # df = test.getQuotes([(0, '000582'), (0, '000584'), (0, '000585'), (0, '000586'), (0, '000587'), (0, '000589'), (0, '000590'), (0, '000591'), (0, '000592'), (0, '000593'), (0, '000595'), (0, '000596'), (0, '000597'), (0, '000598'), (0, '000599'), (0, '000600'), (0, '000601'), (0, '000603'), (0, '000605'), (0, '000606'), (0, '000607'), (0, '000608'), (0, '000609'), (0, '000610'), (0, '000611'), (0, '000612'), (0, '000613'), (0, '000615'), (0, '000616'), (0, '000617'), (0, '000619'), (0, '000620'), (0, '000622'), (0, '000623'), (0, '000625'), (0, '000626'), (0, '000627'), (0, '000628'), (0, '000629'), (0, '000630'), (0, '000631'), (0, '000632'), (0, '000633'), (0, '000635'), (0, '000636'), (0, '000637'), (0, '000638'), (0, '000639'), (0, '000650'), (0, '000651'), (0, '000652'), (0, '000655'), (0, '000656'), (0, '000657'), (0, '000659'), (0, '000661'), (0, '000662'), (0, '000663'), (0, '000665'), (0, '000666'), (0, '000667'), (0, '000668'), (0, '000669'), (0, '000670'), (0, '000671'), (0, '000672'), (0, '000673'), (0, '000676'), (0, '000677'), (0, '000678'), (0, '000679'), (0, '000680'), (0, '000681'), (0, '000682'), (0, '000683'), (0, '000685'), (0, '000686'), (0, '000687'), (0, '000688'), (0, '000690')])
    for key, val in df.iterrows():
        print('%d - %s' % (key, val))
    test.release()
