# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import jqdatasdk as jq
from utils import RetryDecorator
import pandas as pd


class jqdataApi:
    def __init__(self, account, password, retry=3, timeout=30, interval=0.5):
        self.login_status = False
        self.account = account
        self.password = password
        self.retry = retry
        self.timeout = timeout
        self.interval = interval
        jq.auth(self.account, self.password)
        if jq.is_auth():
            self.login_status = True

    def getSignalStockMinuteQuotationByDateRange(self, stock_code, start_date, end_date, fq=None):
        @RetryDecorator(self.retry, self.interval)
        def __local_run():
            return jq.get_price(stock_code,
                                start_date=start_date,
                                end_date=end_date,
                                frequency='1m',
                                fields=['open',
                                        'close',
                                        'low',
                                        'high',
                                        'volume',
                                        'money',
                                        'factor',
                                        'high_limit',
                                        'low_limit',
                                        'avg',
                                        'pre_close',
                                        'paused',
                                        'open_interest'],
                                skip_paused=True,
                                fq=fq,
                                count=None,
                                panel=False,
                                fill_paused=True)
        df = __local_run()
        return df.astype(object).where(pd.notnull(df), None)

    def getAllStocks(self):
        @RetryDecorator(self.retry, self.interval)
        def __local_run():
            return jq.get_all_securities(types=['stock', 'index'])
        df = __local_run()
        return df.astype(object).where(pd.notnull(df), None)

    def getCount(self):
        @RetryDecorator(self.retry, self.interval)
        def __local_run():
            return jq.get_query_count()

        dct = __local_run()
        if dct is not None:
            return int(dct['spare'])
        else:
            return 0


if __name__ == '__main__':
    api = jqdataApi('18780098283', 'Kj_459951958')
    print(api.getCount())

