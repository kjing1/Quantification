import matplotlib.pyplot as plt
import os
import log
from db.dbpool import MyPymysqlPool
import time
import pandas as pd
from enum import Enum


class turnoverRateClasses(Enum):
    LESS_THAN_ONEPERCENT: 0
    ONEPERCENT_TO_THREEPERCENT: 1
    THREEPERCENT_TO_FIVEPERCENT: 2
    FIVEPERCENT_TO_SEVENPERCENT: 3
    SEVENPERCENT_TO_NINEPERCENT: 4
    NINEPERCENT_TO_ELEVENPERCENT: 5
    ELEVENPERCENT_TO_THIRTEENPERCENT: 6
    THIRTEENPERCENT_TO_FIFTEENPERCENT: 7
    FIFTEENPERCENT_TO_SEVENTEENPERCENT: 8
    SEVENTEENPERCENT_TO_NINETEENPERCENT: 9
    NINETEENPERCENT_TO_TWENTYONEPERCENT: 10
    MORE_THAN_TWENTYONEPERCENT: 11


class transactionAmountClasses(Enum):
    LESS_THAN_1000MILLION: 0
    MILLION_X10_TO_X120: 1
    MILLION_X120_TO_X600: 2
    MILLION_X600_TO_X2000: 3
    MILLION_X2000_TO_X5000: 4
    MORE_THAN_5000MILLION: 5


"""
class transactionAmountSubClasses(Enum):


class turnoverRate:
    def __init__(self):
        pass
"""

def is_next_day(dbconn, today, next_day):
    trade_cal = dbconn.getAll('SELECT cal_date, pretrade_date FROM t_exchange_trade_cal t '
                              'WHERE t.is_open=1 and t.pretrade_date = "%s"' % today)
    if trade_cal is not None:
        if trade_cal[0]['cal_date'] == next_day:
            return True
        else:
            return False


def get_limit_up_two_days(logger, dbconn):
    turnover_raterange_list = []
    turnover_rate_list = []
    limit_up_stocks = []
    all_limit_up = dbconn.getAll('SELECT * FROM t_daily t, t_limit_stocks t1 WHERE t.turnover_rate >= 1.0 AND '
                                 't.turnover_rate <= 50 AND t.trade_date >= "20190101" AND t.ts_code = t1.ts_code '
                                 'AND t.trade_date = t1.trade_date and t1.limit="U" GROUP BY t.ts_code')
    if all_limit_up is None:
        return None, turnover_raterange_list, turnover_rate_list

    logger.info('[get_limit_up_two_days] -> START')

    for one in all_limit_up:
        signal_limit_up_count = dbconn.getAll(
            'SELECT * FROM t_daily t, t_limit_stocks t1 WHERE t.ts_code="%s" AND t.turnover_rate >= 1.0 AND '
            't.turnover_rate <= 50 AND t.trade_date >= "20190101" AND t.ts_code = t1.ts_code AND t.trade_date = '
            't1.trade_date and t1.limit="U"' % one['ts_code']
        )
        if signal_limit_up_count is not None:
            if len(signal_limit_up_count) >= 2:
                for i, _ in enumerate(signal_limit_up_count):
                    if i < len(signal_limit_up_count) - 1:
                        if is_next_day(dbconn, signal_limit_up_count[i]['trade_date'],
                                       signal_limit_up_count[i + 1]['trade_date']):
                            tur = float(signal_limit_up_count[i]['turnover_rate'])
                            turnover_rate_list.append(tur)
                            limit_up_stocks.append(signal_limit_up_count[i])
                            # limit_up_stocks.append(signal_limit_up_count[i+1])
                            if 1.0 <= tur < 3.0:
                                #logger.info('(%s-%s-%s) | 1.3' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(1.3)
                            elif 3.0 <= tur < 5.0:
                                #logger.info('(%s-%s-%s) | 3.5' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(3.5)
                            elif 5.0 <= tur < 7.0:
                                #logger.info('(%s-%s-%s) | 5.7' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(5.7)
                            elif 7.0 <= tur < 9.0:
                                #logger.info('(%s-%s-%s) | 7.9' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(7.9)
                            elif 9.0 <= tur < 11.0:
                                #logger.info('(%s-%s-%s) | 9.11' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(9.11)
                            elif 11.0 <= tur < 13.0:
                                #logger.info('(%s-%s-%s) | 11.13' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(11.13)
                            elif 13.0 <= tur < 15.0:
                                #logger.info('(%s-%s-%s) | 13.15' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(13.15)
                            elif 15.0 <= tur < 17.0:
                                #logger.info('(%s-%s-%s) | 15.17' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(15.17)
                            elif 17.0 <= tur < 19.0:
                                #logger.info('(%s-%s-%s) | 17.19' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(17.19)
                            elif 19.0 <= tur < 21.0:
                                #logger.info('(%s-%s-%s) | 19.21' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(19.21)
                            else:
                                #logger.info('(%s-%s-%s) | 21.0' % (
                                #    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                #    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(21.0)
                            break
    logger.info('连续两日及以上涨停的股票换手率在1~3之间: %d -> [%.2f]' % (turnover_raterange_list.count(1.3),
                                                         turnover_raterange_list.count(1.3)/len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在3~5之间: %d -> [%.2f]' % (turnover_raterange_list.count(3.5),
                                                         turnover_raterange_list.count(3.5) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在5~7之间: %d -> [%.2f]' % (turnover_raterange_list.count(5.7),
                                                         turnover_raterange_list.count(5.7) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在7~9之间: %d -> [%.2f]' % (turnover_raterange_list.count(7.9),
                                                         turnover_raterange_list.count(7.9) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在9~11之间: %d -> [%.2f]' % (turnover_raterange_list.count(9.11),
                                                          turnover_raterange_list.count(9.11) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在11~13之间: %d -> [%.2f]' % (turnover_raterange_list.count(11.13),
                                                           turnover_raterange_list.count(11.13) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在13~15之间: %d -> [%.2f]' % (turnover_raterange_list.count(13.15),
                                                           turnover_raterange_list.count(13.15) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在15~17之间: %d -> [%.2f]' % (turnover_raterange_list.count(15.17),
                                                           turnover_raterange_list.count(13.15) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在17~19之间: %d -> [%.2f]' % (turnover_raterange_list.count(17.19),
                                                           turnover_raterange_list.count(17.19) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率在19~21之间: %d -> [%.2f]' % (turnover_raterange_list.count(19.21),
                                                           turnover_raterange_list.count(17.19) / len(turnover_rate_list)))
    logger.info('连续两日及以上涨停的股票换手率大于21: %d -> [%.2f]' % (turnover_raterange_list.count(21.0),
                                                       turnover_raterange_list.count(21.0) / len(turnover_rate_list)))
    logger.info('[get_limit_up_two_days] -> END')
    return limit_up_stocks, turnover_raterange_list, turnover_rate_list


def get_limit_up_amount(all_limit_up_stocks, logger):
    """
    总成交额
    :param all_limit_up_stocks:
    :param logger:
    :return:
    """
    start=0.00
    end=0
    logger.info('[get_limit_up_amount] -> START')
    all_amounts = []
    amounts_count = []
    # 一千万以下
    less_than_10million = []
    # 一千万至1.2亿
    million_x10_to_x120 = []
    # 1.2亿至6亿
    million_x120_to_x600 = []
    # 6亿至20亿
    million_x600_to_x2000 = []
    # 20亿至50亿
    million_x2000_to_x5000 = []
    # 50亿以上
    more_than_5000million = []
    for val in all_limit_up_stocks:
        amount = float(val['amount'])
        if amount is not None:
            # 单位是千元
            all_amounts.append(amount)
            if amount < 10000.00:
                less_than_10million.append(amount)
                amounts_count.append(1.00)
            elif 10000.00 <= amount < 120000.00:
                million_x10_to_x120.append(amount)
                amounts_count.append(2.00)
            elif 120000.00 <= amount < 600000.00:
                million_x120_to_x600.append(amount)
                amounts_count.append(3.00)
            elif 600000.00 <= amount < 2000000.00:
                million_x600_to_x2000.append(amount)
                amounts_count.append(4.00)
            elif 2000000.00 <= amount < 5000000.00:
                million_x2000_to_x5000.append(amount)
                amounts_count.append(5.00)
            else:
                more_than_5000million.append(amount)
                amounts_count.append(6.00)
        else:
            logger.error('%s-%s not found amount' % (val['ts_code'], val['trade_date']))

    logger.info('max value: %f' % max(all_amounts))
    for i in range(int(max(all_amounts))//30000 + 1):
        end = start + 30000.00
        fixed = [x for x in all_amounts if start <= x < end]
        logger.info('总成交额在[%d]至[%d]之间: %d -> [%.2f]' % (start, end, len(fixed), len(fixed) / len(all_amounts)))
        start += 30000.00
    logger.info('[get_limit_up_amount] -> END')
    return all_amounts, amounts_count, less_than_10million, million_x10_to_x120,\
           million_x120_to_x600, million_x600_to_x2000, million_x2000_to_x5000, more_than_5000million


def get_limit_up_total_price(all_limit_up_stocks, logger):
    """
    总市值
    :param all_limit_up_stocks:
    :param logger:
    :return:
    """
    start=0.00
    end=0
    logger.info('[get_limit_up_total_price] -> START')
    all_amounts = []
    amounts_count = []
    # 5亿以下
    less_than_5E = []
    # 5亿至100亿
    million_5E_to_100E = []
    # 100亿至300亿
    million_100E_to_300E = []
    # 300亿至1000亿
    million_300E_to_1000E = []
    # 1000亿以上
    more_than_1000E = []
    for val in all_limit_up_stocks:
        amount = float(val['total_mv'])
        if amount is not None:
            # 单位是万元
            all_amounts.append(amount)
            if amount < 50000.00:
                less_than_5E.append(amount)
                amounts_count.append(1.00)
            elif 50000.00 <= amount < 1000000.00:
                million_5E_to_100E.append(amount)
                amounts_count.append(2.00)
            elif 1000000.00 <= amount < 3000000.00:
                million_100E_to_300E.append(amount)
                amounts_count.append(3.00)
            elif 3000000.00 <= amount < 10000000.00:
                million_300E_to_1000E.append(amount)
                amounts_count.append(4.00)
            else:
                more_than_1000E.append(amount)
                amounts_count.append(5.00)
        else:
            logger.error('%s-%s not found total_mv' % (val['ts_code'], val['trade_date']))

    logger.info('max value: %f' % max(all_amounts))
    for i in range(int(max(all_amounts))//20000 + 1):
        end = start + 20000.00
        fixed = [x for x in all_amounts if start <= x < end]
        logger.info('总市值在[%d]至[%d]之间: %d -> [%.2f]' % (start, end, len(fixed), len(fixed) / len(all_amounts)))
        start += 20000.00
    logger.info('[get_limit_up_total_price] -> END')
    return all_amounts, amounts_count, less_than_5E, million_5E_to_100E,\
           million_100E_to_300E, million_300E_to_1000E, more_than_1000E


def get_limit_up_total_price_circ(all_limit_up_stocks, logger):
    """
    总流通市值
    :param all_limit_up_stocks:
    :param logger:
    :return:
    """
    start=0.00
    end=0
    logger.info('[get_limit_up_total_price_circ] -> START')
    all_amounts = []
    amounts_count = []
    # 5亿以下
    less_than_5E = []
    # 5亿至100亿
    million_5E_to_100E = []
    # 100亿至300亿
    million_100E_to_300E = []
    # 300亿至1000亿
    million_300E_to_1000E = []
    # 1000亿以上
    more_than_1000E = []
    for val in all_limit_up_stocks:
        amount = float(val['circ_mv'])
        if amount is not None:
            # 单位是千元
            all_amounts.append(amount)
            if amount < 50000.00:
                less_than_5E.append(amount)
                amounts_count.append(1.00)
            elif 50000.00 <= amount < 1000000.00:
                million_5E_to_100E.append(amount)
                amounts_count.append(2.00)
            elif 1000000.00 <= amount < 3000000.00:
                million_100E_to_300E.append(amount)
                amounts_count.append(3.00)
            elif 3000000.00 <= amount < 10000000.00:
                million_300E_to_1000E.append(amount)
                amounts_count.append(4.00)
            else:
                more_than_1000E.append(amount)
                amounts_count.append(5.00)
        else:
            logger.error('%s-%s not found circ_mv' % (val['ts_code'], val['trade_date']))

    logger.info('max value: %f' % max(all_amounts))
    for i in range(int(max(all_amounts))//20000 + 1):
        end = start + 20000.00
        fixed = [x for x in all_amounts if start <= x < end]
        logger.info('总流通市值在[%d]至[%d]之间: %d -> [%.2f]' % (start, end, len(fixed), len(fixed) / len(all_amounts)))
        start += 20000.00
    logger.info('[get_limit_up_total_price_circ] -> END')
    return all_amounts, amounts_count, less_than_5E, million_5E_to_100E,\
           million_100E_to_300E, million_300E_to_1000E, more_than_1000E


def open_changes(all_limit_up_stocks, logger):
    """
    开盘幅度
    :return:
    """
    logger.info('[open_changes] -> START')
    pct_chg_all = []
    pct_chg_minus_5 = []
    pct_chg_minus_4 = []
    pct_chg_minus_3 = []
    pct_chg_minus_2 = []
    pct_chg_minus_1 = []
    pct_chg_0 = []
    pct_chg_1 = []
    pct_chg_2 = []
    pct_chg_3 = []
    pct_chg_4 = []
    pct_chg_5 = []
    pct_chg_6 = []
    pct_chg_7 = []
    pct_chg_8 = []
    pct_chg_9 = []
    for d in all_limit_up_stocks:
        pct_chg = float(d['pct_chg'])
        pct_chg_all.append(pct_chg)
        if -5.0 <= pct_chg < -4.0:
            pct_chg_minus_5.append(pct_chg)
        elif -4.0 <= pct_chg < -3.0:
            pct_chg_minus_4.append(pct_chg)
        elif -3.0 <= pct_chg < -2.0:
            pct_chg_minus_3.append(pct_chg)
        elif -2.0 <= pct_chg < -1.0:
            pct_chg_minus_2.append(pct_chg)
        elif -1.0 <= pct_chg < 0:
            pct_chg_minus_1.append(pct_chg)
        elif 0 <= pct_chg < 1:
            pct_chg_0.append(pct_chg)
        elif 1 <= pct_chg < 2:
            pct_chg_1.append(pct_chg)
        elif 2 <= pct_chg < 3:
            pct_chg_2.append(pct_chg)
        elif 3 <= pct_chg < 4:
            pct_chg_3.append(pct_chg)
        elif 4 <= pct_chg < 5:
            pct_chg_4.append(pct_chg)
        elif 5 <= pct_chg < 6:
            pct_chg_5.append(pct_chg)
        elif 6 <= pct_chg < 7:
            pct_chg_6.append(pct_chg)
        elif 7 <= pct_chg < 8:
            pct_chg_7.append(pct_chg)
        elif 8 <= pct_chg < 9:
            pct_chg_8.append(pct_chg)
        elif 9 <= pct_chg:
            pct_chg_9.append(pct_chg)
        else:
            logger.error('unkown pct_chg: %f' % pct_chg)

    logger.info('开盘幅度-5至-4: %d -> [%.2f]' % (len(pct_chg_minus_5), len(pct_chg_minus_5) / len(pct_chg_all)))
    logger.info('开盘幅度-4至-3: %d -> [%.2f]' % (len(pct_chg_minus_4), len(pct_chg_minus_4) / len(pct_chg_all)))
    logger.info('开盘幅度-3至-2: %d -> [%.2f]' % (len(pct_chg_minus_3), len(pct_chg_minus_3) / len(pct_chg_all)))
    logger.info('开盘幅度-2至-1: %d -> [%.2f]' % (len(pct_chg_minus_2), len(pct_chg_minus_2) / len(pct_chg_all)))
    logger.info('开盘幅度-1至0: %d -> [%.2f]' % (len(pct_chg_minus_1), len(pct_chg_minus_1) / len(pct_chg_all)))
    logger.info('开盘幅度0至1: %d -> [%.2f]' % (len(pct_chg_0), len(pct_chg_0) / len(pct_chg_all)))
    logger.info('开盘幅度1至2: %d -> [%.2f]' % (len(pct_chg_1), len(pct_chg_1) / len(pct_chg_all)))
    logger.info('开盘幅度2至3: %d -> [%.2f]' % (len(pct_chg_2), len(pct_chg_2) / len(pct_chg_all)))
    logger.info('开盘幅度3至4: %d -> [%.2f]' % (len(pct_chg_3), len(pct_chg_3) / len(pct_chg_all)))
    logger.info('开盘幅度4至5: %d -> [%.2f]' % (len(pct_chg_4), len(pct_chg_4) / len(pct_chg_all)))
    logger.info('开盘幅度5至6: %d -> [%.2f]' % (len(pct_chg_5), len(pct_chg_5) / len(pct_chg_all)))
    logger.info('开盘幅度6至7: %d -> [%.2f]' % (len(pct_chg_6), len(pct_chg_6) / len(pct_chg_all)))
    logger.info('开盘幅度7至8: %d -> [%.2f]' % (len(pct_chg_7), len(pct_chg_7) / len(pct_chg_all)))
    logger.info('开盘幅度8至9: %d -> [%.2f]' % (len(pct_chg_8), len(pct_chg_8) / len(pct_chg_all)))
    logger.info('开盘幅度9至10: %d -> [%.2f]' % (len(pct_chg_9), len(pct_chg_9) / len(pct_chg_all)))
    logger.info('[open_changes] -> END')
    return pct_chg_all, pct_chg_minus_5, pct_chg_minus_4, pct_chg_minus_3, pct_chg_minus_2, pct_chg_minus_1,\
           pct_chg_0, pct_chg_1, pct_chg_2, pct_chg_3, pct_chg_4, pct_chg_5, pct_chg_6, pct_chg_7, pct_chg_8, pct_chg_9


def limit_up_times(all_limit_up_stocks, logger):
    """
    涨停时间
    :param all_limit_up_stocks:
    :param logger:
    :return:
    """
    logger.info('[limit_up_times] -> START')
    time_925_to_945 = []
    time_925_to_930 = []
    time_930_to_935 = []
    time_935_to_940 = []
    time_940_to_945 = []

    time_945_to_1130 = []
    time_945_to_1000 = []
    time_1000_to_1015 = []
    time_1015_to_1030 = []
    time_1030_to_1045 = []
    time_1045_to_1100 = []
    time_1100_to_1115 = []
    time_1115_to_1130 = []

    time_1300_to_1315 = []
    time_1300_to_1305 = []
    time_1305_to_1310 = []
    time_1310_to_1315 = []

    time_1315_to_1500 = []
    time_1315_to_1330 = []
    time_1330_to_1345 = []
    time_1345_to_1400 = []
    time_1400_to_1415 = []
    time_1415_to_1430 = []
    time_1430_to_1445 = []
    time_1445_to_1500 = []

    for d in all_limit_up_stocks:
        t = d['first_time']
        if t == '' or t is None:
            t = '09:31:00'
        if '09:25:00' <= t < '09:45:00':
            time_925_to_945.append(t)
            if '09:25:00' <= t < '09:30:00':
                time_925_to_930.append(t)
            elif '09:30:00' <= t < '09:35:00':
                time_930_to_935.append(t)
            elif '09:35:00' <= t < '09:40:00':
                time_935_to_940.append(t)
            else:
                time_940_to_945.append(t)
        elif '09:45:00' <= t < '11:30:00':
            time_945_to_1130.append(t)
            if '09:45:00' <= t < '10:00:00':
                time_945_to_1000.append(t)
            elif '10:00:00' <= t < '10:15:00':
                time_1000_to_1015.append(t)
            elif '10:15:00' <= t < '10:30:00':
                time_1015_to_1030.append(t)
            elif '10:30:00' <= t < '10:45:00':
                time_1030_to_1045.append(t)
            elif '10:45:00' <= t < '11:00:00':
                time_1045_to_1100.append(t)
            elif '11:00:00' <= t < '11:15:00':
                time_1100_to_1115.append(t)
            else:
                time_1115_to_1130.append(t)
        elif '13:00:00' <= t < '13:15:00':
            time_1300_to_1315.append(t)
            if '13:00:00' <= t < '13:05:00':
                time_1300_to_1305.append(t)
            elif '13:05:00' <= t < '13:10:00':
                time_1305_to_1310.append(t)
            else:
                time_1310_to_1315.append(t)
        elif '13:15:00' <= t < '15:00:00':
            time_1315_to_1500.append(t)
            if '13:15:00' <= t < '13:30:00':
                time_1315_to_1330.append(t)
            elif '13:30:00' <= t < '13:45:00':
                time_1330_to_1345.append(t)
            elif '13:45:00' <= t < '14:00:00':
                time_1345_to_1400.append(t)
            elif '14:00:00' <= t < '14:15:00':
                time_1400_to_1415.append(t)
            elif '14:15:00' <= t < '14:30:00':
                time_1415_to_1430.append(t)
            elif '14:30:00' <= t < '14:45:00':
                time_1430_to_1445.append(t)
            else:
                time_1445_to_1500.append(t)
        else:
            logger.error('unkown time: %s' % t)

    logger.info('涨停时间在9:25-9:30: %d -> [%.2f]' % (len(time_925_to_930), len(time_925_to_930) / len(all_limit_up_stocks)))
    logger.info('涨停时间在9:30-9:35: %d -> [%.2f]' % (len(time_930_to_935), len(time_930_to_935) / len(all_limit_up_stocks)))
    logger.info('涨停时间在9:35-9:40: %d -> [%.2f]' % (len(time_935_to_940), len(time_935_to_940) / len(all_limit_up_stocks)))
    logger.info('涨停时间在9:40-9:45: %d -> [%.2f]' % (len(time_940_to_945), len(time_940_to_945) / len(all_limit_up_stocks)))
    logger.info('涨停时间在9:45-10:00: %d -> [%.2f]' % (len(time_945_to_1000), len(time_940_to_945) / len(all_limit_up_stocks)))
    logger.info('涨停时间在10:00-10:15: %d -> [%.2f]' % (len(time_1000_to_1015), len(time_1000_to_1015) / len(all_limit_up_stocks)))
    logger.info('涨停时间在10:15-10:30: %d -> [%.2f]' % (len(time_1015_to_1030), len(time_1015_to_1030) / len(all_limit_up_stocks)))
    logger.info('涨停时间在10:30-10:45: %d -> [%.2f]' % (len(time_1030_to_1045), len(time_1030_to_1045) / len(all_limit_up_stocks)))
    logger.info('涨停时间在10:45-11:00: %d -> [%.2f]' % (len(time_1045_to_1100), len(time_1045_to_1100) / len(all_limit_up_stocks)))
    logger.info('涨停时间在11:00-11:15: %d -> [%.2f]' % (len(time_1100_to_1115), len(time_1100_to_1115) / len(all_limit_up_stocks)))
    logger.info('涨停时间在11:15-11:30: %d -> [%.2f]' % (len(time_1115_to_1130), len(time_1115_to_1130) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:00-13:05: %d -> [%.2f]' % (len(time_1300_to_1305), len(time_1300_to_1305) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:05-13:10: %d -> [%.2f]' % (len(time_1305_to_1310), len(time_1305_to_1310) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:10-13:15: %d -> [%.2f]' % (len(time_1310_to_1315), len(time_1310_to_1315) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:15-13:30: %d -> [%.2f]' % (len(time_1315_to_1330), len(time_1315_to_1330) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:30-13:45: %d -> [%.2f]' % (len(time_1330_to_1345), len(time_1330_to_1345) / len(all_limit_up_stocks)))
    logger.info('涨停时间在13:45-14:00: %d -> [%.2f]' % (len(time_1345_to_1400), len(time_1345_to_1400) / len(all_limit_up_stocks)))
    logger.info('涨停时间在14:00-14:15: %d -> [%.2f]' % (len(time_1400_to_1415), len(time_1400_to_1415) / len(all_limit_up_stocks)))
    logger.info('涨停时间在14:15-14:30: %d -> [%.2f]' % (len(time_1415_to_1430), len(time_1415_to_1430) / len(all_limit_up_stocks)))
    logger.info('涨停时间在14:30-14:45: %d -> [%.2f]' % (len(time_1430_to_1445), len(time_1430_to_1445) / len(all_limit_up_stocks)))
    logger.info('涨停时间在14:45-15:00: %d -> [%.2f]' % (len(time_1445_to_1500), len(time_1445_to_1500) / len(all_limit_up_stocks)))
    logger.info('[limit_up_times] -> END')
    return time_925_to_945, time_925_to_930, time_930_to_935, time_935_to_940, time_940_to_945, \
           time_945_to_1130, time_945_to_1000, time_1000_to_1015, time_1015_to_1030, time_1030_to_1045, time_1045_to_1100, \
           time_1300_to_1315, time_1300_to_1305, time_1305_to_1310, time_1310_to_1315, \
           time_1315_to_1500, time_1315_to_1330, time_1330_to_1345, time_1345_to_1400, time_1400_to_1415, time_1415_to_1430, time_1430_to_1445, time_1445_to_1500


def open_prices(all_limit_up_stocks, logger):
    """
    价格
    :param all_limit_up_stocks:
    :param logger:
    :return:
    """
    start=0.00
    logger.info('[open_prices] -> START')
    all_price = []
    price_0_10 = []
    price_10_30 = []
    price_more_than_30 = []
    for d in all_limit_up_stocks:
        price = float(d['open'])
        all_price.append(price)
        if 0 <= price < 10:
            price_0_10.append(price)
        elif 10 <= price < 30:
            price_10_30.append(price)
        else:
            price_more_than_30.append(price)

    logger.info('max value: %f' % max(all_price))
    for i in range(int(max(all_price))//2 + 1):
        fixed = [x for x in all_price if start <= x < start+2.00]
        logger.info('开盘价在[%d]至[%d]之间: %d -> [%.2f]' % (start, start+2.00, len(fixed), len(fixed) / len(all_price)))
        start += 2.00
    logger.info('[open_prices] -> END')
    return price_0_10, price_10_30, price_more_than_30


def bar_with_percentage_plot(x_list, y_list):
    # 绘图参数, 第一个参数是x轴的数据, 第二个参数是y轴的数据,
    # 第三个参数是柱子的大小, 默认值是1(值在0到1之间), color是柱子的颜色, alpha是柱子的透明度
    plt.bar(range(len(x_list)), y_list, 0.4, color='r', alpha=0.8)
    # 添加轴标签
    plt.ylabel('y')
    # 标题
    plt.title('IMG')
    # 添加刻度标签
    plt.xticks(range(len(x_list)), x_list)
    # 设置Y轴的刻度范围
    y_max = max(y_list) + max(y_list) / 2
    # y_max = max(y_list) + max(y_list) / 11
    plt.ylim([0, y_max])
    y_sum = sum(y_list)
    percentage = [x / y_sum for x in y_list]
    # 为每个条形图添加数值标签
    for x, y in enumerate(y_list):
        plt.text(x, y + y_max / 11, str(round(percentage[x], 2)), ha='center')
    # 显示图形
    plt.show()


if __name__ == '__main__':
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    logger = log.init_logging(os.path.join(os.path.expanduser('./logs/'),
                                           'model_%s_%s.txt' % (__name__, today)), 'info')
    dbconn = MyPymysqlPool(logger, 'MysqlDatabaseInfo')
    all_limit_up_stocks, turnover_raterange_list, turnover_rate_list = get_limit_up_two_days(logger, dbconn)
    _, _, _, _, _, _, _, _ = get_limit_up_amount(all_limit_up_stocks, logger)
    _, _, _, _, _, _, _ = get_limit_up_total_price(all_limit_up_stocks, logger)
    _, _, _, _, _, _, _ = get_limit_up_total_price_circ(all_limit_up_stocks, logger)
    _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = open_changes(all_limit_up_stocks, logger)
    _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = limit_up_times(all_limit_up_stocks, logger)
    _, _, _ = open_prices(all_limit_up_stocks, logger)
    exit()

    """
    all_limit_up_stocks, turnover_raterange_list, turnover_rate_list = get_limit_up_two_days(logger, dbconn)
    print(all_limit_up_stocks)

    x_list = ['1%-3%', '3%-5%', '5%-7%', '7%-9%', '9%-11%', '11%-13%', '13%-15%', '15%-17%', '17%-19%', '19%-21%',
              '21%+']
    y_list = [turnover_raterange_list.count(1.3), turnover_raterange_list.count(3.5),
              turnover_raterange_list.count(5.7), turnover_raterange_list.count(7.9),
              turnover_raterange_list.count(9.11), turnover_raterange_list.count(11.13),
              turnover_raterange_list.count(13.15), turnover_raterange_list.count(15.17),
              turnover_raterange_list.count(17.19), turnover_raterange_list.count(19.21),
              turnover_raterange_list.count(21.0)]
    bar_with_percentage_plot(x_list, y_list)

    _, amounts_count, _, _, _, _, _, _  = get_limit_up_amount(all_limit_up_stocks, logger)
    x_list = ['less than 100mil', '100mil-1.2E', '1.2E-6E', '6E-20E', '20E-50E', 'more than 1000E']
    y_list = [amounts_count.count(1.0), amounts_count.count(2.0), amounts_count.count(3.0),
              amounts_count.count(4.0), amounts_count.count(5.0), amounts_count.count(6.0)]
    bar_with_percentage_plot(x_list, y_list)

    _, price_count, _, _, _, _, _ = get_limit_up_total_price(all_limit_up_stocks, logger)
    x_list = ['less than 5E', '5E-100E', '100E-300E', '300E-1000E', 'more than 1000E']
    y_list = [price_count.count(1.0), price_count.count(2.0), price_count.count(3.0),
              price_count.count(4.0), price_count.count(5.0)]
    bar_with_percentage_plot(x_list, y_list)

    _, price_count, _, _, _, _, _ = get_limit_up_total_price_circ(all_limit_up_stocks, logger)
    x_list = ['less than 5E', '5E-100E', '100E-300E', '300E-1000E', 'more than 1000E']
    y_list = [price_count.count(1.0), price_count.count(2.0), price_count.count(3.0),
              price_count.count(4.0), price_count.count(5.0)]
    bar_with_percentage_plot(x_list, y_list)

    all_changes, m5, m4, m3, m2, m1, u0, u1, u2, u3, u4, u5, u6, u7, u8, u9 = open_changes(all_limit_up_stocks, logger)
    x_list = ['-5--4', '-4--3', '-3--2', '-2--1', '-1-0',
              '0-1', '1-2', '2-3', '3-4', '4-5',
              '5-6', '6-7', '7-8', '8-9', '9-10']
    y_list = [len(m5), len(m4), len(m3), len(m2), len(m1),
              len(u0), len(u1), len(u2), len(u3), len(u4), len(u5),
              len(u6), len(u7), len(u8), len(u9)]
    bar_with_percentage_plot(x_list, y_list)

    _, t1, t2, t3, t4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = limit_up_times(all_limit_up_stocks, logger)
    x_list = ['9:25-9:30', '9:30-9:35', '9:35-9:40', '9:40-9:45']
    y_list = [len(t1), len(t2), len(t3), len(t4)]
    bar_with_percentage_plot(x_list, y_list)

    _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = limit_up_times(all_limit_up_stocks, logger)
    x_list = ['9:25-9:30', '9:30-9:35', '9:35-9:40', '9:40-9:45']
    y_list = [len(t1), len(t2), len(t3), len(t4)]
    bar_with_percentage_plot(x_list, y_list)
    """
