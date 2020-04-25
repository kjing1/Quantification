# python 3.7.4
# coding = utf-8
# filename predict.py
# author 463714869@qq.com, create by VIM at 2019/11/6

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
from db import dbpool
from ml import train as tp
import log


def pred(model_path, x):
    model = tf.keras.models.load_model(model_path)
    p = model.predict(x)

    return p


def get_newer_five_data(tscode, seq_len=5):
    x = []
    conn = dbpool.MyPymysqlPool(None, 'MysqlDatabaseInfo')
    datas = conn.getAll('SELECT * FROM (SELECT trade_date, `open`, high, low, `close`, `change`, pct_chg, vol,'
                        ' amount, turnover_rate, turnover_rate_f, '
                        'volume_ratio, pe, pe_ttm, pb, ps, ps_ttm,'
                        ' total_share, float_share, free_share, total_mv, '
                        'circ_mv FROM t_daily WHERE ts_code="%s" order by trade_date desc limit 5)'
                        ' a ORDER BY trade_date' % tscode)
    if len(datas) != 5:
        return None
    for data in datas:
        tmp = [data['open'],
               data['high'],
               data['low'],
               data['close'],
               data['change'],
               data['pct_chg'],
               data['vol'],
               data['amount'],
               data['turnover_rate'],
               data['volume_ratio'],
               data['total_share'],
               data['float_share'],
               data['free_share'],
               data['total_mv'],
               data['circ_mv']]
        x.append(tmp)
    x = np.reshape(np.array(x, dtype='float_'), (1, seq_len, len(tmp)))
    return x


if __name__ == '__main__':
    stocks_list = []
    file_path = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\ml\\stocks_price.txt'
    logger = log.init_logging(file_path, 'info')
    # 链接数据库
    conn = dbpool.MyPymysqlPool(None, 'MysqlDatabaseInfo')
    # 获取股票ts代码
    for d in conn.getAll('select ts_code from t_stocks'):
        stocks_list.append(d['ts_code'])
    conn.dispose()

    logger.info('tscode\tpred_price\tchange')
    for stock in stocks_list:
        x = get_newer_five_data(stock, tp.TIMESTEP)
        if x is None:
            continue
        _, price = tp.train(stock, save=False, pred=True, x=x)
        logger.info('%s\t%f\t%f' % (stock, float(price), (float(price)-x[0][-1][3]) / float(x[0][-1][3])))
