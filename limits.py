from tus_batch_business import batchBusiness
import matplotlib as mpl
import matplotlib.pyplot as plt


def is_next_day(api, today, next_day):
    trade_cal = api.dbconn.getAll('select cal_date, pretrade_date from t_exchange_trade_cal t where t.is_open=1 and t.pretrade_date = "%s"' % today)
    if trade_cal is not None:
        if trade_cal[0]['cal_date'] == next_day:
            return True
        else:
            return False


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
    turnover_raterange_list = []
    turnover_rate_list = []
    with open('.\\logs\\tus_batch_business_20200426.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            flags = float(line.replace(' ', '').split('|')[1])
            turnover_rate_list.append(float(line.replace(' ', '').split('-')[2].split(')')[0]))
            if flags == 1.3:
                turnover_raterange_list.append(1.3)
            elif flags == 3.5:
                turnover_raterange_list.append(3.5)
            elif flags == 5.7:
                turnover_raterange_list.append(5.7)
            elif flags == 7.9:
                turnover_raterange_list.append(7.9)
            elif flags == 9.11:
                turnover_raterange_list.append(9.11)
            elif flags == 11.13:
                turnover_raterange_list.append(11.13)
            elif flags == 13.15:
                turnover_raterange_list.append(13.15)
            elif flags == 15.17:
                turnover_raterange_list.append(15.17)
            elif flags == 17.19:
                turnover_raterange_list.append(17.19)
            elif flags == 19.21:
                turnover_raterange_list.append(19.21)
            else:
                turnover_raterange_list.append(21.0)
    x_list = ['1%-3%', '3%-5%', '5%-7%', '7%-9%', '9%-11%', '11%-13%', '13%-15%', '15%-17%', '17%-19%', '19%-21%', '21%+']
    y_list = []
    y_list.append(turnover_raterange_list.count(1.3))
    y_list.append(turnover_raterange_list.count(3.5))
    y_list.append(turnover_raterange_list.count(5.7))
    y_list.append(turnover_raterange_list.count(7.9))
    y_list.append(turnover_raterange_list.count(9.11))
    y_list.append(turnover_raterange_list.count(11.13))
    y_list.append(turnover_raterange_list.count(13.15))
    y_list.append(turnover_raterange_list.count(15.17))
    y_list.append(turnover_raterange_list.count(17.19))
    y_list.append(turnover_raterange_list.count(19.21))
    y_list.append(turnover_raterange_list.count(21.0))
    bar_with_percentage_plot(x_list, y_list)
    exit(0)
    api = batchBusiness('', '', '', None)
    all_limit_up = api.dbconn.getAll('SELECT * FROM t_daily t, t_limit_stocks t1 WHERE t.turnover_rate >= 1.0 AND '
                                     't.turnover_rate <= 50 AND t.trade_date >= "20190101" AND t.ts_code = t1.ts_code '
                                     'AND t.trade_date = t1.trade_date and t1.limit="U" GROUP BY t.ts_code')
    turnover_rate_list = []
    for one in all_limit_up:
        signal_limit_up_count = api.dbconn.getAll(
            'SELECT * FROM t_daily t, t_limit_stocks t1 WHERE t.ts_code="%s" AND t.turnover_rate >= 1.0 AND '
            't.turnover_rate <= 50 AND t.trade_date >= "20190101" AND t.ts_code = t1.ts_code AND t.trade_date = '
            't1.trade_date and t1.limit="U"' % one['ts_code']
        )
        if signal_limit_up_count is not None:
            if len(signal_limit_up_count) >= 2:
                for i, _ in enumerate(signal_limit_up_count):
                    if i < len(signal_limit_up_count) - 1:
                        if is_next_day(api, signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i+1]['trade_date']):
                            tur = float(signal_limit_up_count[i]['turnover_rate'])
                            turnover_rate_list.append(tur)
                            if 1.0 <= tur < 3.0:
                                api.logger.info('(%s-%s-%s) | 1*3' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 3.0 <= tur < 5.0:
                                api.logger.info('(%s-%s-%s) | 3*5' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 5.0 <= tur < 7.0:
                                api.logger.info('(%s-%s-%s) | 5*7' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 7.0 <= tur < 9.0:
                                api.logger.info('(%s-%s-%s) | 7*9' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 9.0 <= tur < 11.0:
                                api.logger.info('(%s-%s-%s) | 9*11' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 11.0 <= tur < 13.0:
                                api.logger.info('(%s-%s-%s) | 11*13' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 13.0 <= tur < 15.0:
                                api.logger.info('(%s-%s-%s) | 13*15' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 15.0 <= tur < 17.0:
                                api.logger.info('(%s-%s-%s) | 15*17' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 17.0 <= tur < 19.0:
                                api.logger.info('(%s-%s-%s) | 17*19' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            elif 19.0 <= tur < 21.0:
                                api.logger.info('(%s-%s-%s) | 19*21' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            else:
                                api.logger.info('(%s-%s-%s) | 21+' % (one['ts_code'], signal_limit_up_count[i]['trade_date'], signal_limit_up_count[i]['turnover_rate']))
                            """
                            for d in signal_limit_up_count[i:i+2]:
                                api.logger.info('{}'.format(d))
                            """
                            break
