# python 3.7.4
# coding = utf-8
# filename datasets.py
# author 463714869@qq.com, create by VIM at 2019/11/5

from __future__ import absolute_import, division, print_function, unicode_literals

from db import dbpool
import numpy as np


def make_train_test_data_by_tscode(tscode, seq_len=5):
    x = []
    y = []
    train_x = []
    train_y = []
    conn = dbpool.MyPymysqlPool(None, 'MysqlDatabaseInfo')
    datas = conn.getAll('SELECT `open`, high, low, `close`, `change`, pct_chg, '
                        'vol, amount, turnover_rate, turnover_rate_f, '
                        'volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, total_share, float_share, free_share, total_mv, '
                        'circ_mv FROM t_daily WHERE ts_code="%s"' % tscode)
    conn.dispose()
    if datas is not None:
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
            if tmp.count('nan') or tmp.count('inf') or tmp.count('') or tmp.count('None'):
                continue
            x.append(tmp)
            y.append(data['close'])

    for i in range(len(x) - seq_len):
        train_x.append(x[i: i + seq_len])
        train_y.append(y[i + seq_len])
    train_x = np.array(train_x, dtype='float_')
    train_y = np.array(train_y, dtype='float_')

    ind = int(len(train_x) * 0.8)
    return x, y, len(train_x[0][0]), train_x[:ind, :, :], train_y[:ind], train_x[ind:, :, :], train_y[ind:]


if __name__ == '__main__':
    a, b, l, c, d, e, f = make_train_test_data_by_tscode('000004.SZ')
    print(l)
    print(len(a))
    print(len(b))
    print(c.shape)
    print(d.shape)
    print(e.shape)
    print(f.shape)
