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
                                logger.info('(%s-%s-%s) | 1.3' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(1.3)
                            elif 3.0 <= tur < 5.0:
                                logger.info('(%s-%s-%s) | 3.5' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(3.5)
                            elif 5.0 <= tur < 7.0:
                                logger.info('(%s-%s-%s) | 5.7' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(5.7)
                            elif 7.0 <= tur < 9.0:
                                logger.info('(%s-%s-%s) | 7.9' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(7.9)
                            elif 9.0 <= tur < 11.0:
                                logger.info('(%s-%s-%s) | 9.11' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(9.11)
                            elif 11.0 <= tur < 13.0:
                                logger.info('(%s-%s-%s) | 11.13' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(11.13)
                            elif 13.0 <= tur < 15.0:
                                logger.info('(%s-%s-%s) | 13.15' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(13.15)
                            elif 15.0 <= tur < 17.0:
                                logger.info('(%s-%s-%s) | 15.17' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(15.17)
                            elif 17.0 <= tur < 19.0:
                                logger.info('(%s-%s-%s) | 17.19' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(17.19)
                            elif 19.0 <= tur < 21.0:
                                logger.info('(%s-%s-%s) | 19.21' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(19.21)
                            else:
                                logger.info('(%s-%s-%s) | 21.0' % (
                                    one['ts_code'], signal_limit_up_count[i]['trade_date'],
                                    signal_limit_up_count[i]['turnover_rate']))
                                turnover_raterange_list.append(21.0)
                            break

    return limit_up_stocks, turnover_raterange_list, turnover_rate_list


def get_limit_up_amount(all_limit_up_stocks, logger):
    all_amounts = []
    amounts_count = []
    """
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
    """
    for key, val in all_limit_up_stocks.iterrows():
        result = float(val['amount'])
        if result is not None:
            # 单位是千元
            amount = float(result['amount'])
            all_amounts.append(amount)
            if amount < 10000.00:
                # less_than_10million.append(amount)
                amounts_count.append(1.00)
            elif 10000.00 <= amount < 120000.00:
                # million_x10_to_x120.append(amount)
                amounts_count.append(2.00)
            elif 120000.00 <= amount < 600000.00:
                # million_x120_to_x600.append(amount)
                amounts_count.append(3.00)
            elif 600000.00 <= amount < 2000000.00:
                # million_x600_to_x2000.append(amount)
                amounts_count.append(4.00)
            elif 2000000.00 <= amount < 5000000.00:
                # million_x2000_to_x5000.append(amount)
                amounts_count.append(5.00)
            else:
                # more_than_5000million.append(amount)
                amounts_count.append(9.00)
        else:
            logger.error('%s-%s not found amount' % (val['ts_code'], val['trade_date']))

    return all_amounts, amounts_count


def get_limit_up_total_price():
    pass


def bar_with_percentage_plot(x_list, y_list):
    # 绘图参数, 第一个参数是x轴的数据, 第二个参数是y轴的数据,
    # 第三个参数是柱子的大小, 默认值是1(值在0到1之间), color是柱子的颜色, alpha是柱子的透明度
    plt.bar(range(len(x_list)), y_list, 0.4, color='r', alpha=0.8)
    # 添加轴标签
    plt.ylabel('y轴')
    # 标题
    plt.title('柱状图添加百分比')
    # 添加刻度标签
    plt.xticks(range(len(x_list)), x_list)
    # 设置Y轴的刻度范围
    y_max = max(y_list)
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

    all_amounts, amounts_count = get_limit_up_amount(all_limit_up_stocks, logger)
    x_list = ['less than 100mil', '100mil-1.2E', '1.2E-6E',
              '6E-20E', '20E-50E', '50E-100E', '100E-300E', '300E-1000E', 'more than 1000E']
    y_list = [amounts_count.count(1.0), amounts_count.count(2.0), amounts_count.count(3.0),
              amounts_count.count(4.0), amounts_count.count(5.0), amounts_count.count(6.0),
              amounts_count.count(7.0), amounts_count.count(8.0), amounts_count.count(9.0)]
    bar_with_percentage_plot(x_list, y_list)
