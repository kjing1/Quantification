# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import tushare as ts
from utils import funcRetry, Retry
import time
import sys

MYTOKEN = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'


class tusApi:
    """
    封装tushare api, 增加重试
    """

    def __init__(self, token, retry=3, timeout=30, intv=1):
        self.token_ = token
        ts.set_token(self.token_)
        self.pro = ts.pro_api()
        self.timeout = timeout
        self.intv = intv
        self.retry = retry

    def getSignalStockDailyQuantByDate(self, stock_code, start_date, end_date):
        """
        通过股票代码获取指定时间段的原始日行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 原始日行情df
        """
        df = funcRetry(self.pro.daily, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date)
        return df

    def getAllStockDailyQuantByDate(self, trade_date):
        """
        根据指定的日期获取所有股票的原始日行情
        :param trade_date: 交易日期, 格式: 20200101
        :return: 原始日行情df
        """
        df = funcRetry(self.pro.daily, self.retry, self.intv, trade_date=trade_date)
        return df

    def getSignalStockWeeklyQuantByDate(self, stock_code, start_date, end_date):
        """
        通过股票代码获取指定时间段的原始周行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 原始周行情df
        """
        df = funcRetry(self.pro.weekly, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        return df

    def getAllStockWeeklyQuantByDate(self, trade_date):
        """
        根据指定的日期获取所有股票的原始周行情
        :param trade_date: 交易日期, 格式: 20200101
        :return: 原始周行情df
        """
        df = funcRetry(self.pro.weekly, self.retry, self.intv, trade_date=trade_date,
                       fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        return df

    def getSignalStockMonthlyQuantByDate(self, stock_code, start_date, end_date):
        """
        通过股票代码获取指定时间段的原始月行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 原始月行情df
        """
        df = funcRetry(self.pro.monthly, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        return df

    def getAllStockMonthlyQuantByDate(self, trade_date):
        """
        根据指定的日期获取所有股票的原始月行情
        :param trade_date: 交易日期, 格式: 20200101
        :return: 原始月行情df
        """
        df = funcRetry(self.pro.monthly, self.retry, self.intv, trade_date=trade_date,
                       fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        return df

    def getAllStockBaseInformation(self):
        """
        获取所有股票的基础信息
        :return: 所有股票基础信息df
        """
        df = funcRetry(self.pro.stock_basic,
                       self.retry,
                       self.intv,
                       exchange='',
                       list_status='',
                       fields='ts_code,'
                              'symbol,'
                              'name,'
                              'area,'
                              'industry,'
                              'list_date,'
                              'fullname,'
                              'enname,'
                              'market,'
                              'exchange,'
                              'curr_type,'
                              'list_status,'
                              'delist_date,'
                              'is_hs')
        return df

    # TODO: 增加按日期范围获取数据
    def getSuspendStocksByDate(self, trade_date):
        """
        获取指定日期停盘的股票信息
        :param trade_date: 日期, 格式: 20200202
        :return: df, 出错返回None
        """
        df = funcRetry(self.pro.suspend_d, self.retry, self.intv,
                       trade_date=trade_date,
                       suspend_type='S',
                       fields='ts_code, trade_date, suspend_timing, suspend_type')
        return df

    # TODO: 增加按日期范围获取数据
    def getRestartStocksByDate(self, trade_date):
        """
        获取指定日期复盘的股票信息
        :param trade_date: 日期, 格式: 20200202
        :return: df, 出错返回None
        """
        df = funcRetry(self.pro.suspend_d, self.retry, self.intv,
                       trade_date=trade_date,
                       suspend_type='R',
                       fields='ts_code, trade_date, suspend_timing, suspend_type')
        return df

    def getSignalStockMoneyFlowByDate(self, stock_code, start_date, end_date):
        """
        获取个股指定时间段的资金流向
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 例如: 20200202
        :param end_date: 结束日期, 例如: 20200202
        :return: 资金流向df, 出错返回None
        """
        df = funcRetry(self.pro.moneyflow, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,trade_date,buy_sm_vol,buy_sm_amount,sell_sm_vol,sell_sm_amount,buy_md_vol,'
                              'buy_md_amount,sell_md_vol,sell_md_amount,buy_lg_vol,buy_lg_amount,sell_lg_vol,'
                              'sell_lg_amount,buy_elg_vol,buy_elg_amount,sell_elg_vol,sell_elg_amount,net_mf_vol,'
                              'net_mf_amount')
        return df

    def getAllStockMoneyFlowByDate(self, trade_date):
        """
        获取所有股票在指定日期的资金流向
        :param trade_date: 日期, 格式: 20200202
        :return: 资金流向df, 出错返回None
        """
        df = funcRetry(self.pro.moneyflow, self.retry, self.intv, trade_date=trade_date,
                       fields='ts_code,trade_date,buy_sm_vol,buy_sm_amount,sell_sm_vol,sell_sm_amount,buy_md_vol,'
                              'buy_md_amount,sell_md_vol,sell_md_amount,buy_lg_vol,buy_lg_amount,sell_lg_vol,'
                              'sell_lg_amount,buy_elg_vol,buy_elg_amount,sell_elg_vol,sell_elg_amount,net_mf_vol,'
                              'net_mf_amount')
        return df

    def getSignalStockLimitPriceByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票在指定时间段的涨跌停价格
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 涨跌停df, 出错返回None
        """
        df = funcRetry(self.pro.stk_limit, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='trade_date,ts_code,pre_close,up_limit,down_limit')
        return df

    def getAllStockLimitPriceByDate(self, trade_date):
        """
        获取指定日期所有股票的涨跌停价格
        :param trade_date: 日期, 格式: 20200202
        :return: 涨跌停df, 出错返回None
        """
        df = funcRetry(self.pro.stk_limit, self.retry, self.intv, trade_date=trade_date,
                       fields='trade_date,ts_code,pre_close,up_limit,down_limit')
        return df

    def getAllStockLimitUpStocksByDate(self, trade_date):
        """
        获取指定日期涨停的股票
        :param trade_date: 日期, 格式: 20200202
        :return: 股票df, 出错返回None
        """
        df = funcRetry(self.pro.limit_list, self.retry, self.intv,
                       trade_date=trade_date,
                       limit_type='U',
                       fields='trade_date,'
                              'ts_code,'
                              'name,'
                              'close,'
                              'pct_chg,'
                              'amp,'
                              'fc_ratio,'
                              'fl_ratio,'
                              'fd_amount,'
                              'first_time,'
                              'last_time,'
                              'open_times,'
                              'strth,'
                              'limit')
        return df

    def getSignalStockLimitUpStocksByDate(self, stock_code, start_date, end_date):
        """
        获取指定日期涨停的股票
        :param end_date:
        :param start_date:
        :param stock_code:
        :return: 股票df, 出错返回None
        """
        df = funcRetry(self.pro.limit_list, self.retry, self.intv,
                       ts_code=stock_code,
                       start_date=start_date,
                       end_date=end_date,
                       limit_type='U',
                       fields='trade_date,'
                              'ts_code,'
                              'name,'
                              'close,'
                              'pct_chg,'
                              'amp,'
                              'fc_ratio,'
                              'fl_ratio,'
                              'fd_amount,'
                              'first_time,'
                              'last_time,'
                              'open_times,'
                              'strth,'
                              'limit')
        return df

    def getAllStockLimitDownStocksByDate(self, trade_date):
        """
        获取指定日期跌停的股票
        :param trade_date: 日期, 格式: 20200202
        :return: 股票df, 出错返回None
        """
        df = funcRetry(self.pro.limit_list, self.retry, self.intv,
                       trade_date=trade_date,
                       limit_type='D',
                       fields='trade_date,'
                              'ts_code,'
                              'name,'
                              'close,'
                              'pct_chg,'
                              'amp,'
                              'fc_ratio,'
                              'fl_ratio,'
                              'fd_amount,'
                              'first_time,'
                              'last_time,'
                              'open_times,'
                              'strth,'
                              'limit')
        return df

    def getSignalStockLimitDownStocksByDate(self, stock_code, start_date, end_date):
        """
        获取指定日期跌停的股票
        :param end_date:
        :param start_date:
        :param stock_code:
        :return: 股票df, 出错返回None
        """
        df = funcRetry(self.pro.limit_list, self.retry, self.intv,
                       ts_code=stock_code,
                       start_date=start_date,
                       end_date=end_date,
                       limit_type='D',
                       fields='trade_date,'
                              'ts_code,'
                              'name,'
                              'close,'
                              'pct_chg,'
                              'amp,'
                              'fc_ratio,'
                              'fl_ratio,'
                              'fd_amount,'
                              'first_time,'
                              'last_time,'
                              'open_times,'
                              'strth,'
                              'limit')
        return df

    def get24HFlashNews(self, src, start_date, end_date):
        """
        获取指定时间段的24小时快讯
        :param start_date: 开始日期，格式为：2020-01-01 23:11:11
        :param end_date: 结束日期，格式同startdate
        :param src: 渠道
                    sina: 新浪财经
                    wallstreetcn: 华尔街见闻
                    10jqka: 同花顺
                    eastmoney: 东方财富
                    yuncaijing: 云财经
        :return: 快讯df
        """
        df = funcRetry(self.pro.news,
                       self.retry,
                       self.intv,
                       src=src, start_date=start_date, end_date=end_date, fields='title,content,datetime,channels')
        return df

    def getMajorNews(self, start_date, end_date, src=''):
        """
        获取指定时间段的长篇新闻
        :param start_date: 开始日期，格式为：2020-01-01 23:11:11
        :param end_date: 结束日期，格式同startdate
        :param src: 渠道, 为空则查询所有
                    sina: 新浪财经
                    wallstreetcn: 华尔街见闻
                    10jqka: 同花顺
                    eastmoney: 东方财富
                    yuncaijing: 云财经
        :return: 长篇新闻df
        """
        df = funcRetry(self.pro.major_news,
                       self.retry,
                       self.intv,
                       src=src, start_date=start_date, end_date=end_date, fields='title,content,pub_time,src')
        return df

    def getSignalStockAdjFactorByDate(self, stock_code, start_date, end_date):
        """
        根据指定的日期获取指定股票的复权因子
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 交易日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 复权因子df
        """
        df = funcRetry(self.pro.adj_factor, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date)
        return df

    def getAllStockAdjFactorByDate(self, trade_date):
        """
        根据指定的日期获取指定股票的复权因子
        :param trade_date: 交易日期, 格式: 20200101
        :return: 复权因子df
        """
        df = funcRetry(self.pro.adj_factor, self.retry, self.intv, ts_code='', trade_date=trade_date)
        return df

    def getSignalStockQFQDailyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的前复权日行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 前复权日行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='qfq', asset='E')
        return df

    def getSignalStockHFQDailyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的后复权日行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 后复权日行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='hfq', asset='E')
        return df

    def getSignalStockQFQWeeklyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的前复权周行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 前复权周行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='qfq', asset='E', freq='W')
        return df

    def getSignalStockHFQWeeklyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的后复权周行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 后复权周行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='hfq', asset='E', freq='W')
        return df

    def getSignalStockQFQMonthlyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的前复权月行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 前复权月行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='qfq', asset='E', freq='M')
        return df

    def getSignalStockHFQMonthlyQuantByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的后复权月行情
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 后复权月行情df
        """
        df = funcRetry(ts.pro_bar, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date, adj='hfq', asset='E', freq='M')
        return df

    def getSignalStockDailyIndexByDate(self, stock_code, start_date, end_date):
        """
        获取指定股票对应时间段的日指数情况
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200101
        :param end_date: 结束日期, 格式: 20200101
        :return: 日指数df
        """
        df = funcRetry(self.pro.daily_basic, self.retry, self.intv,
                       ts_code=stock_code,
                       trade_date='',
                       start_date=start_date,
                       end_date=end_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'turnover_rate,'
                              'turnover_rate_f,'
                              'volume_ratio,'
                              'pe,'
                              'pe_ttm,'
                              'pb,'
                              'ps,'
                              'ps_ttm,'
                              'dv_ratio,'
                              'dv_ttm,'
                              'total_share,'
                              'float_share,'
                              'free_share,'
                              'total_mv,'
                              'circ_mv')
        return df

    def getAllStockDailyIndexByDate(self, trade_date):
        """
        获取所有股票指定日期的指数情况
        :param trade_date: 日期, 格式: 20200202
        :return: 日指数df
        """
        df = funcRetry(self.pro.daily_basic, self.retry, self.intv,
                       ts_code='',
                       trade_date=trade_date,
                       start_date='',
                       end_date='',
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'turnover_rate,'
                              'turnover_rate_f,'
                              'volume_ratio,'
                              'pe,'
                              'pe_ttm,'
                              'pb,'
                              'ps,'
                              'ps_ttm,'
                              'dv_ratio,'
                              'dv_ttm,'
                              'total_share,'
                              'float_share,'
                              'free_share,'
                              'total_mv,'
                              'circ_mv')
        return df

    def getCompanyBaseInformationByExchange(self, exchange='SZSE'):
        """
        根据交易所获取所有上市公司的基础信息
        :param exchange: 交易所, SZSE - 深圳, SSE - 上海
        :return: 上市公司基础信息df
        """
        df = funcRetry(self.pro.stock_company, self.retry, self.intv,
                       exchange='SZSE',
                       fields='ts_code,'
                              'exchange,'
                              'chairman,'
                              'manager,'
                              'secretary,'
                              'reg_capital,'
                              'setup_date,'
                              'province,'
                              'city,'
                              'introduction,'
                              'website,'
                              'email,'
                              'office,'
                              'employees,'
                              'main_business,'
                              'business_scope')
        return df

    def getCompanyManagers(self, stock_code):
        """
        获取指定上市公司的所有管理层信息
        :param stock_code: 股票代码, 例如: 000001.SZ
        :return: 管理层信息df, 出错返回None
        """
        df = funcRetry(self.pro.stk_managers, self.retry, self.intv, ts_code=stock_code,
                       fields='ts_code,ann_date,name,gender,lev,title,edu,national,birthday,begin_date,end_date,resume')
        return df

    def getAllStockTradeCalendarByDate(self, start_date, end_date):
        """
        获取所有股票的交易日历
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 交易日历df, 出错返回None
        """
        df = funcRetry(self.pro.trade_cal, self.retry, self.intv,
                       exchange='', start_date=start_date, end_date=end_date,
                       fields='exchange,cal_date,is_open,pretrade_date')
        return df

    def getSignalStockProfitByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票指定时间段的利润表数据
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 利润表df, 出错返回None
        """
        df = funcRetry(self.pro.income, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'report_type,'
                              'comp_type,'
                              'basic_eps,'
                              'diluted_eps,'
                              'total_revenue,'
                              'revenue,'
                              'int_income,'
                              'prem_earned,'
                              'comm_income,'
                              'n_commis_income,'
                              'n_oth_income,'
                              'n_oth_b_income,'
                              'prem_income,'
                              'out_prem,'
                              'une_prem_reser,'
                              'reins_income,'
                              'n_sec_tb_income,'
                              'n_sec_uw_income,'
                              'n_asset_mg_income,'
                              'oth_b_income,'
                              'fv_value_chg_gain,'
                              'invest_income,'
                              'ass_invest_income,'
                              'forex_gain,'
                              'total_cogs,'
                              'oper_cost,'
                              'int_exp,'
                              'comm_exp,'
                              'biz_tax_surchg,'
                              'sell_exp,'
                              'admin_exp,'
                              'fin_exp,'
                              'assets_impair_loss,'
                              'prem_refund,'
                              'compens_payout,'
                              'reser_insur_liab,'
                              'div_payt,'
                              'reins_exp,'
                              'oper_exp,'
                              'compens_payout_refu,'
                              'insur_reser_refu,'
                              'reins_cost_refund,'
                              'other_bus_cost,'
                              'operate_profit,'
                              'non_oper_income,'
                              'non_oper_exp,'
                              'nca_disploss,'
                              'total_profit,'
                              'income_tax,'
                              'n_income,'
                              'n_income_attr_p,'
                              'minority_gain,'
                              'oth_compr_income,'
                              't_compr_income,'
                              'compr_inc_attr_p,'
                              'compr_inc_attr_m_s,'
                              'ebit,'
                              'ebitda,'
                              'insurance_exp,'
                              'undist_profit,'
                              'distable_profit,'
                              'update_flag')
        return df

    def getAllStockProfitByDate(self, start_date, end_date):
        """
        获取所有股票指定时间段的利润表数据
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 利润表df, 出错返回None
        """
        df = funcRetry(self.pro.income_vip, self.retry, self.intv,
                       start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'report_type,'
                              'comp_type,'
                              'basic_eps,'
                              'diluted_eps,'
                              'total_revenue,'
                              'revenue,'
                              'int_income,'
                              'prem_earned,'
                              'comm_income,'
                              'n_commis_income,'
                              'n_oth_income,'
                              'n_oth_b_income,'
                              'prem_income,'
                              'out_prem,'
                              'une_prem_reser,'
                              'reins_income,'
                              'n_sec_tb_income,'
                              'n_sec_uw_income,'
                              'n_asset_mg_income,'
                              'oth_b_income,'
                              'fv_value_chg_gain,'
                              'invest_income,'
                              'ass_invest_income,'
                              'forex_gain,'
                              'total_cogs,'
                              'oper_cost,'
                              'int_exp,'
                              'comm_exp,'
                              'biz_tax_surchg,'
                              'sell_exp,'
                              'admin_exp,'
                              'fin_exp,'
                              'assets_impair_loss,'
                              'prem_refund,'
                              'compens_payout,'
                              'reser_insur_liab,'
                              'div_payt,'
                              'reins_exp,'
                              'oper_exp,'
                              'compens_payout_refu,'
                              'insur_reser_refu,'
                              'reins_cost_refund,'
                              'other_bus_cost,'
                              'operate_profit,'
                              'non_oper_income,'
                              'non_oper_exp,'
                              'nca_disploss,'
                              'total_profit,'
                              'income_tax,'
                              'n_income,'
                              'n_income_attr_p,'
                              'minority_gain,'
                              'oth_compr_income,'
                              't_compr_income,'
                              'compr_inc_attr_p,'
                              'compr_inc_attr_m_s,'
                              'ebit,'
                              'ebitda,'
                              'insurance_exp,'
                              'undist_profit,'
                              'distable_profit,'
                              'update_flag')
        return df

    def getSignalStockBalanceSheetByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票指定时间段的资产负债表数据
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 资产负债表df, 出错返回None
        """
        df = funcRetry(self.pro.balancesheet, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'report_type,'
                              'comp_type,'
                              'total_share,'
                              'cap_rese,'
                              'undistr_porfit,'
                              'surplus_rese,'
                              'special_rese,'
                              'money_cap,'
                              'trad_asset,'
                              'notes_receiv,'
                              'accounts_receiv,'
                              'oth_receiv,'
                              'prepayment,'
                              'div_receiv,'
                              'int_receiv,'
                              'inventories,'
                              'amor_exp,'
                              'nca_within_1y,'
                              'sett_rsrv,'
                              'loanto_oth_bank_fi,'
                              'premium_receiv,'
                              'reinsur_receiv,'
                              'reinsur_res_receiv,'
                              'pur_resale_fa,'
                              'oth_cur_assets,'
                              'total_cur_assets,'
                              'fa_avail_for_sale,'
                              'htm_invest,'
                              'lt_eqt_invest,'
                              'invest_real_estate,'
                              'time_deposits,'
                              'oth_assets,'
                              'lt_rec,'
                              'fix_assets,'
                              'cip,'
                              'const_materials,'
                              'fixed_assets_disp,'
                              'produc_bio_assets,'
                              'oil_and_gas_assets,'
                              'intan_assets,'
                              'r_and_d,'
                              'goodwill,'
                              'lt_amor_exp,'
                              'defer_tax_assets,'
                              'decr_in_disbur,'
                              'oth_nca,'
                              'total_nca,'
                              'cash_reser_cb,'
                              'depos_in_oth_bfi,'
                              'prec_metals,'
                              'deriv_assets,'
                              'rr_reins_une_prem,'
                              'rr_reins_outstd_cla,'
                              'rr_reins_lins_liab,'
                              'rr_reins_lthins_liab,'
                              'refund_depos,'
                              'ph_pledge_loans,'
                              'refund_cap_depos,'
                              'indep_acct_assets,'
                              'client_depos,'
                              'client_prov,'
                              'transac_seat_fee,'
                              'invest_as_receiv,'
                              'total_assets,'
                              'lt_borr,'
                              'st_borr,'
                              'cb_borr,'
                              'depos_ib_deposits,'
                              'loan_oth_bank,'
                              'trading_fl,'
                              'notes_payable,'
                              'acct_payable,'
                              'adv_receipts,'
                              'sold_for_repur_fa,'
                              'comm_payable,'
                              'payroll_payable,'
                              'taxes_payable,'
                              'int_payable,'
                              'div_payable,'
                              'oth_payable,'
                              'acc_exp,'
                              'deferred_inc,'
                              'st_bonds_payable,'
                              'payable_to_reinsurer,'
                              'rsrv_insur_cont,'
                              'acting_trading_sec,'
                              'acting_uw_sec,'
                              'non_cur_liab_due_1y,'
                              'oth_cur_liab,'
                              'total_cur_liab,'
                              'bond_payable,'
                              'lt_payable,'
                              'specific_payables,'
                              'estimated_liab,'
                              'defer_tax_liab,'
                              'defer_inc_non_cur_liab,'
                              'oth_ncl,'
                              'total_ncl,'
                              'depos_oth_bfi,'
                              'deriv_liab,'
                              'depos,'
                              'agency_bus_liab,'
                              'oth_liab,'
                              'prem_receiv_adva,'
                              'depos_received,'
                              'ph_invest,'
                              'reser_une_prem,'
                              'reser_outstd_claims,'
                              'reser_lins_liab,'
                              'reser_lthins_liab,'
                              'indept_acc_liab,'
                              'pledge_borr,'
                              'indem_payable,'
                              'policy_div_payable,'
                              'total_liab,'
                              'treasury_share,'
                              'ordin_risk_reser,'
                              'forex_differ,'
                              'invest_loss_unconf,'
                              'minority_int,'
                              'total_hldr_eqy_exc_min_int,'
                              'total_hldr_eqy_inc_min_int,'
                              'total_liab_hldr_eqy,'
                              'lt_payroll_payable,'
                              'oth_comp_income,'
                              'oth_eqt_tools,'
                              'oth_eqt_tools_p_shr,'
                              'lending_funds,'
                              'acc_receivable,'
                              'st_fin_payable,'
                              'payables,'
                              'hfs_assets,'
                              'hfs_sales,'
                              'update_flag')
        return df

    def getAllStockBalanceSheetByDate(self, start_date, end_date):
        """
        获取全部股票指定时间段的资产负债表数据
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 资产负债表df, 出错返回None
        """
        df = funcRetry(self.pro.balancesheet_vip, self.retry, self.intv,
                       start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'report_type,'
                              'comp_type,'
                              'total_share,'
                              'cap_rese,'
                              'undistr_porfit,'
                              'surplus_rese,'
                              'special_rese,'
                              'money_cap,'
                              'trad_asset,'
                              'notes_receiv,'
                              'accounts_receiv,'
                              'oth_receiv,'
                              'prepayment,'
                              'div_receiv,'
                              'int_receiv,'
                              'inventories,'
                              'amor_exp,'
                              'nca_within_1y,'
                              'sett_rsrv,'
                              'loanto_oth_bank_fi,'
                              'premium_receiv,'
                              'reinsur_receiv,'
                              'reinsur_res_receiv,'
                              'pur_resale_fa,'
                              'oth_cur_assets,'
                              'total_cur_assets,'
                              'fa_avail_for_sale,'
                              'htm_invest,'
                              'lt_eqt_invest,'
                              'invest_real_estate,'
                              'time_deposits,'
                              'oth_assets,'
                              'lt_rec,'
                              'fix_assets,'
                              'cip,'
                              'const_materials,'
                              'fixed_assets_disp,'
                              'produc_bio_assets,'
                              'oil_and_gas_assets,'
                              'intan_assets,'
                              'r_and_d,'
                              'goodwill,'
                              'lt_amor_exp,'
                              'defer_tax_assets,'
                              'decr_in_disbur,'
                              'oth_nca,'
                              'total_nca,'
                              'cash_reser_cb,'
                              'depos_in_oth_bfi,'
                              'prec_metals,'
                              'deriv_assets,'
                              'rr_reins_une_prem,'
                              'rr_reins_outstd_cla,'
                              'rr_reins_lins_liab,'
                              'rr_reins_lthins_liab,'
                              'refund_depos,'
                              'ph_pledge_loans,'
                              'refund_cap_depos,'
                              'indep_acct_assets,'
                              'client_depos,'
                              'client_prov,'
                              'transac_seat_fee,'
                              'invest_as_receiv,'
                              'total_assets,'
                              'lt_borr,'
                              'st_borr,'
                              'cb_borr,'
                              'depos_ib_deposits,'
                              'loan_oth_bank,'
                              'trading_fl,'
                              'notes_payable,'
                              'acct_payable,'
                              'adv_receipts,'
                              'sold_for_repur_fa,'
                              'comm_payable,'
                              'payroll_payable,'
                              'taxes_payable,'
                              'int_payable,'
                              'div_payable,'
                              'oth_payable,'
                              'acc_exp,'
                              'deferred_inc,'
                              'st_bonds_payable,'
                              'payable_to_reinsurer,'
                              'rsrv_insur_cont,'
                              'acting_trading_sec,'
                              'acting_uw_sec,'
                              'non_cur_liab_due_1y,'
                              'oth_cur_liab,'
                              'total_cur_liab,'
                              'bond_payable,'
                              'lt_payable,'
                              'specific_payables,'
                              'estimated_liab,'
                              'defer_tax_liab,'
                              'defer_inc_non_cur_liab,'
                              'oth_ncl,'
                              'total_ncl,'
                              'depos_oth_bfi,'
                              'deriv_liab,'
                              'depos,'
                              'agency_bus_liab,'
                              'oth_liab,'
                              'prem_receiv_adva,'
                              'depos_received,'
                              'ph_invest,'
                              'reser_une_prem,'
                              'reser_outstd_claims,'
                              'reser_lins_liab,'
                              'reser_lthins_liab,'
                              'indept_acc_liab,'
                              'pledge_borr,'
                              'indem_payable,'
                              'policy_div_payable,'
                              'total_liab,'
                              'treasury_share,'
                              'ordin_risk_reser,'
                              'forex_differ,'
                              'invest_loss_unconf,'
                              'minority_int,'
                              'total_hldr_eqy_exc_min_int,'
                              'total_hldr_eqy_inc_min_int,'
                              'total_liab_hldr_eqy,'
                              'lt_payroll_payable,'
                              'oth_comp_income,'
                              'oth_eqt_tools,'
                              'oth_eqt_tools_p_shr,'
                              'lending_funds,'
                              'acc_receivable,'
                              'st_fin_payable,'
                              'payables,'
                              'hfs_assets,'
                              'hfs_sales,'
                              'update_flag')
        return df

    def getSignalStockCashflowByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票指定时间段的现金流量表数据
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 现金流量表df, 出错返回None
        """
        df = funcRetry(self.pro.cashflow, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'comp_type,'
                              'report_type,'
                              'net_profit,'
                              'finan_exp,'
                              'c_fr_sale_sg,'
                              'recp_tax_rends,'
                              'n_depos_incr_fi,'
                              'n_incr_loans_cb,'
                              'n_inc_borr_oth_fi,'
                              'prem_fr_orig_contr,'
                              'n_incr_insured_dep,'
                              'n_reinsur_prem,'
                              'n_incr_disp_tfa,'
                              'ifc_cash_incr,'
                              'n_incr_disp_faas,'
                              'n_incr_loans_oth_bank,'
                              'n_cap_incr_repur,'
                              'c_fr_oth_operate_a,'
                              'c_inf_fr_operate_a,'
                              'c_paid_goods_s,'
                              'c_paid_to_for_empl,'
                              'c_paid_for_taxes,'
                              'n_incr_clt_loan_adv,'
                              'n_incr_dep_cbob,'
                              'c_pay_claims_orig_inco,'
                              'pay_handling_chrg,'
                              'pay_comm_insur_plcy,'
                              'oth_cash_pay_oper_act,'
                              'st_cash_out_act,'
                              'n_cashflow_act,'
                              'oth_recp_ral_inv_act,'
                              'c_disp_withdrwl_invest,'
                              'c_recp_return_invest,'
                              'n_recp_disp_fiolta,'
                              'n_recp_disp_sobu,'
                              'stot_inflows_inv_act,'
                              'c_pay_acq_const_fiolta,'
                              'c_paid_invest,'
                              'n_disp_subs_oth_biz,'
                              'oth_pay_ral_inv_act,'
                              'n_incr_pledge_loan,'
                              'stot_out_inv_act,'
                              'n_cashflow_inv_act,'
                              'c_recp_borrow,'
                              'proc_issue_bonds,'
                              'oth_cash_recp_ral_fnc_act,'
                              'stot_cash_in_fnc_act,'
                              'free_cashflow,'
                              'c_prepay_amt_borr,'
                              'c_pay_dist_dpcp_int_exp,'
                              'incl_dvd_profit_paid_sc_ms,'
                              'oth_cashpay_ral_fnc_act,'
                              'stot_cashout_fnc_act,'
                              'n_cash_flows_fnc_act,'
                              'eff_fx_flu_cash,'
                              'n_incr_cash_cash_equ,'
                              'c_cash_equ_beg_period,'
                              'c_cash_equ_end_period,'
                              'c_recp_cap_contrib,'
                              'incl_cash_rec_saims,'
                              'uncon_invest_loss,'
                              'prov_depr_assets,'
                              'depr_fa_coga_dpba,'
                              'amort_intang_assets,'
                              'lt_amort_deferred_exp,'
                              'decr_deferred_exp,'
                              'incr_acc_exp,'
                              'loss_disp_fiolta,'
                              'loss_scr_fa,'
                              'loss_fv_chg,'
                              'invest_loss,'
                              'decr_def_inc_tax_assets,'
                              'incr_def_inc_tax_liab,'
                              'decr_inventories,'
                              'decr_oper_payable,'
                              'incr_oper_payable,'
                              'others,'
                              'im_net_cashflow_oper_act,'
                              'conv_debt_into_cap,'
                              'conv_copbonds_due_within_1y,'
                              'fa_fnc_leases,'
                              'end_bal_cash,'
                              'beg_bal_cash,'
                              'end_bal_cash_equ,'
                              'beg_bal_cash_equ,'
                              'im_n_incr_cash_equ,'
                              'update_flag')
        return df

    def getAllStockCashflowByDate(self, start_date, end_date):
        """
        获取全部股票指定时间段的现金流量表数据
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 现金流量表df, 出错返回None
        """
        df = funcRetry(self.pro.cashflow_vip, self.retry, self.intv,
                       start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'f_ann_date,'
                              'end_date,'
                              'comp_type,'
                              'report_type,'
                              'net_profit,'
                              'finan_exp,'
                              'c_fr_sale_sg,'
                              'recp_tax_rends,'
                              'n_depos_incr_fi,'
                              'n_incr_loans_cb,'
                              'n_inc_borr_oth_fi,'
                              'prem_fr_orig_contr,'
                              'n_incr_insured_dep,'
                              'n_reinsur_prem,'
                              'n_incr_disp_tfa,'
                              'ifc_cash_incr,'
                              'n_incr_disp_faas,'
                              'n_incr_loans_oth_bank,'
                              'n_cap_incr_repur,'
                              'c_fr_oth_operate_a,'
                              'c_inf_fr_operate_a,'
                              'c_paid_goods_s,'
                              'c_paid_to_for_empl,'
                              'c_paid_for_taxes,'
                              'n_incr_clt_loan_adv,'
                              'n_incr_dep_cbob,'
                              'c_pay_claims_orig_inco,'
                              'pay_handling_chrg,'
                              'pay_comm_insur_plcy,'
                              'oth_cash_pay_oper_act,'
                              'st_cash_out_act,'
                              'n_cashflow_act,'
                              'oth_recp_ral_inv_act,'
                              'c_disp_withdrwl_invest,'
                              'c_recp_return_invest,'
                              'n_recp_disp_fiolta,'
                              'n_recp_disp_sobu,'
                              'stot_inflows_inv_act,'
                              'c_pay_acq_const_fiolta,'
                              'c_paid_invest,'
                              'n_disp_subs_oth_biz,'
                              'oth_pay_ral_inv_act,'
                              'n_incr_pledge_loan,'
                              'stot_out_inv_act,'
                              'n_cashflow_inv_act,'
                              'c_recp_borrow,'
                              'proc_issue_bonds,'
                              'oth_cash_recp_ral_fnc_act,'
                              'stot_cash_in_fnc_act,'
                              'free_cashflow,'
                              'c_prepay_amt_borr,'
                              'c_pay_dist_dpcp_int_exp,'
                              'incl_dvd_profit_paid_sc_ms,'
                              'oth_cashpay_ral_fnc_act,'
                              'stot_cashout_fnc_act,'
                              'n_cash_flows_fnc_act,'
                              'eff_fx_flu_cash,'
                              'n_incr_cash_cash_equ,'
                              'c_cash_equ_beg_period,'
                              'c_cash_equ_end_period,'
                              'c_recp_cap_contrib,'
                              'incl_cash_rec_saims,'
                              'uncon_invest_loss,'
                              'prov_depr_assets,'
                              'depr_fa_coga_dpba,'
                              'amort_intang_assets,'
                              'lt_amort_deferred_exp,'
                              'decr_deferred_exp,'
                              'incr_acc_exp,'
                              'loss_disp_fiolta,'
                              'loss_scr_fa,'
                              'loss_fv_chg,'
                              'invest_loss,'
                              'decr_def_inc_tax_assets,'
                              'incr_def_inc_tax_liab,'
                              'decr_inventories,'
                              'decr_oper_payable,'
                              'incr_oper_payable,'
                              'others,'
                              'im_net_cashflow_oper_act,'
                              'conv_debt_into_cap,'
                              'conv_copbonds_due_within_1y,'
                              'fa_fnc_leases,'
                              'end_bal_cash,'
                              'beg_bal_cash,'
                              'end_bal_cash_equ,'
                              'beg_bal_cash_equ,'
                              'im_n_incr_cash_equ,'
                              'update_flag')
        return df

    def getSignalStockExpressNewsByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票指定时间段的业绩快讯表数据
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 业绩快讯df, 出错返回None
        """
        df = funcRetry(self.pro.express, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'end_date,'
                              'revenue,'
                              'operate_profit,'
                              'total_profit,'
                              'n_income,'
                              'total_assets,'
                              'total_hldr_eqy_exc_min_int,'
                              'diluted_eps,'
                              'diluted_roe,'
                              'yoy_net_profit,'
                              'bps,'
                              'yoy_sales,'
                              'yoy_op,'
                              'yoy_tp,'
                              'yoy_dedu_np,'
                              'yoy_eps,'
                              'yoy_roe,'
                              'growth_assets,'
                              'yoy_equity,'
                              'growth_bps,'
                              'or_last_year,'
                              'op_last_year,'
                              'tp_last_year,'
                              'np_last_year,'
                              'eps_last_year,'
                              'open_net_assets,'
                              'open_bps,'
                              'perf_summary,'
                              'is_audit,'
                              'remark')
        return df

    def getAllStockExpressNewsByDate(self, start_date, end_date):
        """
        获取全部股票指定时间段的业绩快讯表数据
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 业绩快讯df, 出错返回None
        """
        df = funcRetry(self.pro.express_vip, self.retry, self.intv,
                       start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'end_date,'
                              'revenue,'
                              'operate_profit,'
                              'total_profit,'
                              'n_income,'
                              'total_assets,'
                              'total_hldr_eqy_exc_min_int,'
                              'diluted_eps,'
                              'diluted_roe,'
                              'yoy_net_profit,'
                              'bps,'
                              'yoy_sales,'
                              'yoy_op,'
                              'yoy_tp,'
                              'yoy_dedu_np,'
                              'yoy_eps,'
                              'yoy_roe,'
                              'growth_assets,'
                              'yoy_equity,'
                              'growth_bps,'
                              'or_last_year,'
                              'op_last_year,'
                              'tp_last_year,'
                              'np_last_year,'
                              'eps_last_year,'
                              'open_net_assets,'
                              'open_bps,'
                              'perf_summary,'
                              'is_audit,'
                              'remark')
        return df

    def getSignalStockFinanceIndicatorByDate(self, stock_code, start_date, end_date):
        """
        获取单只股票指定时间段的财务指标数据
        :param stock_code: 股票代码, 例如: 000001.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 财务指标df, 出错返回None
        """
        df = funcRetry(self.pro.fina_indicator, self.retry, self.intv,
                       ts_code=stock_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'end_date,'
                              'eps,'
                              'dt_eps,'
                              'total_revenue_ps,'
                              'revenue_ps,'
                              'capital_rese_ps,'
                              'surplus_rese_ps,'
                              'undist_profit_ps,'
                              'extra_item,'
                              'profit_dedt,'
                              'gross_margin,'
                              'current_ratio,'
                              'quick_ratio,'
                              'cash_ratio,'
                              'invturn_days,'
                              'arturn_days,'
                              'inv_turn,'
                              'ar_turn,'
                              'ca_turn,'
                              'fa_turn,'
                              'assets_turn,'
                              'op_income,'
                              'valuechange_income,'
                              'interst_income,'
                              'daa,'
                              'ebit,'
                              'ebitda,'
                              'fcff,'
                              'fcfe,'
                              'current_exint,'
                              'noncurrent_exint,'
                              'interestdebt,'
                              'netdebt,'
                              'tangible_asset,'
                              'working_capital,'
                              'networking_capital,'
                              'invest_capital,'
                              'retained_earnings,'
                              'diluted2_eps,'
                              'bps,'
                              'ocfps,'
                              'retainedps,'
                              'cfps,'
                              'ebit_ps,'
                              'fcff_ps,'
                              'fcfe_ps,'
                              'netprofit_margin,'
                              'grossprofit_margin,'
                              'cogs_of_sales,'
                              'expense_of_sales,'
                              'profit_to_gr,'
                              'saleexp_to_gr,'
                              'adminexp_of_gr,'
                              'finaexp_of_gr,'
                              'impai_ttm,'
                              'gc_of_gr,'
                              'op_of_gr,'
                              'ebit_of_gr,'
                              'roe,'
                              'roe_waa,'
                              'roe_dt,'
                              'roa,'
                              'npta,'
                              'roic,'
                              'roe_yearly,'
                              'roa2_yearly,'
                              'roe_avg,'
                              'opincome_of_ebt,'
                              'investincome_of_ebt,'
                              'n_op_profit_of_ebt,'
                              'tax_to_ebt,'
                              'dtprofit_to_profit,'
                              'salescash_to_or,'
                              'ocf_to_or,'
                              'ocf_to_opincome,'
                              'capitalized_to_da,'
                              'debt_to_assets,'
                              'assets_to_eqt,'
                              'dp_assets_to_eqt,'
                              'ca_to_assets,'
                              'nca_to_assets,'
                              'tbassets_to_totalassets,'
                              'int_to_talcap,'
                              'eqt_to_talcapital,'
                              'currentdebt_to_debt,'
                              'longdeb_to_debt,'
                              'ocf_to_shortdebt,'
                              'debt_to_eqt,'
                              'eqt_to_debt,'
                              'eqt_to_interestdebt,'
                              'tangibleasset_to_debt,'
                              'tangasset_to_intdebt,'
                              'tangibleasset_to_netdebt,'
                              'ocf_to_debt,'
                              'ocf_to_interestdebt,'
                              'ocf_to_netdebt,'
                              'ebit_to_interest,'
                              'longdebt_to_workingcapital,'
                              'ebitda_to_debt,'
                              'turn_days,'
                              'roa_yearly,'
                              'roa_dp,'
                              'fixed_assets,'
                              'profit_prefin_exp,'
                              'non_op_profit,'
                              'op_to_ebt,'
                              'nop_to_ebt,'
                              'ocf_to_profit,'
                              'cash_to_liqdebt,'
                              'cash_to_liqdebt_withinterest,'
                              'op_to_liqdebt,'
                              'op_to_debt,'
                              'roic_yearly,'
                              'total_fa_trun,'
                              'profit_to_op,'
                              'q_opincome,'
                              'q_investincome,'
                              'q_dtprofit,'
                              'q_eps,'
                              'q_netprofit_margin,'
                              'q_gsprofit_margin,'
                              'q_exp_to_sales,'
                              'q_profit_to_gr,'
                              'q_saleexp_to_gr,'
                              'q_adminexp_to_gr,'
                              'q_finaexp_to_gr,'
                              'q_impair_to_gr_ttm,'
                              'q_gc_to_gr,'
                              'q_op_to_gr,'
                              'q_roe,'
                              'q_dt_roe,'
                              'q_npta,'
                              'q_opincome_to_ebt,'
                              'q_investincome_to_ebt,'
                              'q_dtprofit_to_profit,'
                              'q_salescash_to_or,'
                              'q_ocf_to_sales,'
                              'q_ocf_to_or,'
                              'basic_eps_yoy,'
                              'dt_eps_yoy,'
                              'cfps_yoy,'
                              'op_yoy,'
                              'ebt_yoy,'
                              'netprofit_yoy,'
                              'dt_netprofit_yoy,'
                              'ocf_yoy,'
                              'roe_yoy,'
                              'bps_yoy,'
                              'assets_yoy,'
                              'eqt_yoy,'
                              'tr_yoy,'
                              'or_yoy,'
                              'q_gr_yoy,'
                              'q_gr_qoq,'
                              'q_sales_yoy,'
                              'q_sales_qoq,'
                              'q_op_yoy,'
                              'q_op_qoq,'
                              'q_profit_yoy,'
                              'q_profit_qoq,'
                              'q_netprofit_yoy,'
                              'q_netprofit_qoq,'
                              'equity_yoy,'
                              'rd_exp,'
                              'update_flag')
        return df

    def getAllStockFinanceIndicatorByDate(self, start_date, end_date):
        """
        获取单只股票指定时间段的财务指标数据
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 财务指标df, 出错返回None
        """
        df = funcRetry(self.pro.fina_indicator_vip, self.retry, self.intv,
                       start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'ann_date,'
                              'end_date,'
                              'eps,'
                              'dt_eps,'
                              'total_revenue_ps,'
                              'revenue_ps,'
                              'capital_rese_ps,'
                              'surplus_rese_ps,'
                              'undist_profit_ps,'
                              'extra_item,'
                              'profit_dedt,'
                              'gross_margin,'
                              'current_ratio,'
                              'quick_ratio,'
                              'cash_ratio,'
                              'invturn_days,'
                              'arturn_days,'
                              'inv_turn,'
                              'ar_turn,'
                              'ca_turn,'
                              'fa_turn,'
                              'assets_turn,'
                              'op_income,'
                              'valuechange_income,'
                              'interst_income,'
                              'daa,'
                              'ebit,'
                              'ebitda,'
                              'fcff,'
                              'fcfe,'
                              'current_exint,'
                              'noncurrent_exint,'
                              'interestdebt,'
                              'netdebt,'
                              'tangible_asset,'
                              'working_capital,'
                              'networking_capital,'
                              'invest_capital,'
                              'retained_earnings,'
                              'diluted2_eps,'
                              'bps,'
                              'ocfps,'
                              'retainedps,'
                              'cfps,'
                              'ebit_ps,'
                              'fcff_ps,'
                              'fcfe_ps,'
                              'netprofit_margin,'
                              'grossprofit_margin,'
                              'cogs_of_sales,'
                              'expense_of_sales,'
                              'profit_to_gr,'
                              'saleexp_to_gr,'
                              'adminexp_of_gr,'
                              'finaexp_of_gr,'
                              'impai_ttm,'
                              'gc_of_gr,'
                              'op_of_gr,'
                              'ebit_of_gr,'
                              'roe,'
                              'roe_waa,'
                              'roe_dt,'
                              'roa,'
                              'npta,'
                              'roic,'
                              'roe_yearly,'
                              'roa2_yearly,'
                              'roe_avg,'
                              'opincome_of_ebt,'
                              'investincome_of_ebt,'
                              'n_op_profit_of_ebt,'
                              'tax_to_ebt,'
                              'dtprofit_to_profit,'
                              'salescash_to_or,'
                              'ocf_to_or,'
                              'ocf_to_opincome,'
                              'capitalized_to_da,'
                              'debt_to_assets,'
                              'assets_to_eqt,'
                              'dp_assets_to_eqt,'
                              'ca_to_assets,'
                              'nca_to_assets,'
                              'tbassets_to_totalassets,'
                              'int_to_talcap,'
                              'eqt_to_talcapital,'
                              'currentdebt_to_debt,'
                              'longdeb_to_debt,'
                              'ocf_to_shortdebt,'
                              'debt_to_eqt,'
                              'eqt_to_debt,'
                              'eqt_to_interestdebt,'
                              'tangibleasset_to_debt,'
                              'tangasset_to_intdebt,'
                              'tangibleasset_to_netdebt,'
                              'ocf_to_debt,'
                              'ocf_to_interestdebt,'
                              'ocf_to_netdebt,'
                              'ebit_to_interest,'
                              'longdebt_to_workingcapital,'
                              'ebitda_to_debt,'
                              'turn_days,'
                              'roa_yearly,'
                              'roa_dp,'
                              'fixed_assets,'
                              'profit_prefin_exp,'
                              'non_op_profit,'
                              'op_to_ebt,'
                              'nop_to_ebt,'
                              'ocf_to_profit,'
                              'cash_to_liqdebt,'
                              'cash_to_liqdebt_withinterest,'
                              'op_to_liqdebt,'
                              'op_to_debt,'
                              'roic_yearly,'
                              'total_fa_trun,'
                              'profit_to_op,'
                              'q_opincome,'
                              'q_investincome,'
                              'q_dtprofit,'
                              'q_eps,'
                              'q_netprofit_margin,'
                              'q_gsprofit_margin,'
                              'q_exp_to_sales,'
                              'q_profit_to_gr,'
                              'q_saleexp_to_gr,'
                              'q_adminexp_to_gr,'
                              'q_finaexp_to_gr,'
                              'q_impair_to_gr_ttm,'
                              'q_gc_to_gr,'
                              'q_op_to_gr,'
                              'q_roe,'
                              'q_dt_roe,'
                              'q_npta,'
                              'q_opincome_to_ebt,'
                              'q_investincome_to_ebt,'
                              'q_dtprofit_to_profit,'
                              'q_salescash_to_or,'
                              'q_ocf_to_sales,'
                              'q_ocf_to_or,'
                              'basic_eps_yoy,'
                              'dt_eps_yoy,'
                              'cfps_yoy,'
                              'op_yoy,'
                              'ebt_yoy,'
                              'netprofit_yoy,'
                              'dt_netprofit_yoy,'
                              'ocf_yoy,'
                              'roe_yoy,'
                              'bps_yoy,'
                              'assets_yoy,'
                              'eqt_yoy,'
                              'tr_yoy,'
                              'or_yoy,'
                              'q_gr_yoy,'
                              'q_gr_qoq,'
                              'q_sales_yoy,'
                              'q_sales_qoq,'
                              'q_op_yoy,'
                              'q_op_qoq,'
                              'q_profit_yoy,'
                              'q_profit_qoq,'
                              'q_netprofit_yoy,'
                              'q_netprofit_qoq,'
                              'equity_yoy,'
                              'rd_exp,'
                              'update_flag')
        return df

    def getTopList(self, trade_date):
        """
        根据日期获取龙虎榜
        :param trade_date: 日期, 格式: 20200202
        :return: 龙虎榜df, 出错返回None
        """
        df = funcRetry(self.pro.top_list, self.retry, self.intv, trade_date=trade_date,
                       fields='trade_date,ts_code,name,close,pct_change,turnover_rate,amount,l_sell,l_buy,l_amount,'
                              'net_amount,net_rate,amount_rate,float_values,reason')
        return df

    def getTopListTradeDetail(self, trade_date):
        """
        根据日期获取龙虎榜机构交易明细
        :param trade_date: 日期, 格式: 20200202
        :return: 龙虎榜交易明细df, 出错返回None
        """
        df = funcRetry(self.pro.top_inst, self.retry, self.intv, trade_date=trade_date,
                       fields='trade_date,ts_code,exalter,buy,buy_rate,sell,sell_rate,net_buy')
        return df

    def getConcept(self):
        """
        获取概念股分类明细
        :return: 概念股df, 出错返回None
        """
        df = funcRetry(self.pro.concept, self.retry, self.intv, src='ts', fields='code,name,src')
        return df

    def getConceptByStock(self, stock_code):
        """
        查询某只股票的所属概念
        :param stock_code: 股票代码, 例如: 000001.SZ
        :return: 概念股df, 出错返回None
        """
        df = funcRetry(self.pro.concept_detail, self.retry, self.intv,
                       ts_code=stock_code,
                       fields='id,concept_name,ts_code,name,in_date,out_date')
        return df

    # TODO: 批量业务？
    def getConceptById(self, concept_id):
        """
        根据概念分类ID获取所有股票
        :param concept_id: getConcept返回的概念ID
        :return: 概念股df, 出错返回None
        """
        df = funcRetry(self.pro.concept_detail, self.retry, self.intv,
                       id=concept_id,
                       fields='id,concept_name,ts_code,name,in_date,out_date')
        return df

    def getAllStockBigTradeDetailByDate(self, trade_date):
        """
        根据日期获取当日大宗交易明细
        :param trade_date: 交易日期, 格式: 20200202
        :return: 大宗交易df, 出错返回None
        """
        df = funcRetry(self.pro.block_trade, self.retry, self.intv, trade_date=trade_date,
                       fields='ts_code,trade_date,price,vol,amount,buyer,seller')
        return df

    def getSignalStockBigTradeDetailByDate(self, stock_code, start_date, end_date):
        """
        根据日期获取当日大宗交易明细
        :param end_date:
        :param start_date:
        :param stock_code:
        :return: 大宗交易df, 出错返回None
        """
        df = funcRetry(self.pro.block_trade, self.retry, self.intv,
                       ts_code=stock_code,
                       start_date=start_date,
                       end_date=end_date,
                       fields='ts_code,trade_date,price,vol,amount,buyer,seller')
        return df

    def getIndexBasicInformation(self, market):
        """
        根据指定市场获取所有指数信息
        :param market: 市场
                        MSCI	MSCI指数
                        CSI	中证指数
                        SSE	上交所指数
                        SZSE	深交所指数
                        CICC	中金指数
                        SW	申万指数
                        OTH	其他指数
        :return: 基础指数信息df, 出错返回None
        """
        df = funcRetry(self.pro.index_basic, self.retry, self.intv,
                       market=market,
                       fields='ts_code,name,fullname,market,publisher,index_type,category,base_date,base_point,'
                              'list_date,weight_rule,desc,exp_date')
        return df

    def getSignalIndexDailyQuantByDate(self, index_code, start_date, end_date):
        """
        获取单只指数在指定时间段的原始日行情
        :param index_code: 指数代码, 例如: 399300.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 原始日行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_daily, self.retry, self.intv,
                       ts_code=index_code, start_date=start_date, end_date=end_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getAllIndexDailyQuantByDate(self, trade_date):
        """
        获取所有指数在指定时间的原始日行情
        :param trade_date: 日期, 格式: 20200202
        :return: 原始日行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_daily, self.retry, self.intv,
                       trade_date=trade_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getSignalIndexWeeklyQuantByDate(self, index_code, start_date, end_date):
        """
        获取单只指数在指定时间段的原始周行情
        :param index_code: 指数代码, 例如: 399300.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 原始周行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_weekly, self.retry, self.intv,
                       ts_code=index_code,
                       start_date=start_date,
                       end_date=end_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getAllIndexWeeklyQuantByDate(self, trade_date):
        """
        获取单只指数在指定时间段的原始周行情
        :param trade_date: 日期, 格式: 20200202
        :return: 原始周行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_weekly, self.retry, self.intv,
                       trade_date=trade_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getSignalIndexMonthlyQuantByDate(self, index_code, start_date, end_date):
        """
        获取单只指数在指定时间段的原始月行情
        :param index_code: 指数代码, 例如: 399300.SZ
        :param start_date: 开始日期, 格式: 20200202
        :param end_date: 结束日期, 格式: 20200202
        :return: 原始月行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_monthly, self.retry, self.intv,
                       ts_code=index_code,
                       start_date=start_date,
                       end_date=end_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getAllIndexMonthlyQuantByDate(self, trade_date):
        """
        获取单只指数在指定时间段的原始月行情
        :param trade_date: 日期, 格式: 20200202
        :return: 原始月行情df, 出错返回None
        """
        df = funcRetry(self.pro.index_monthly, self.retry, self.intv,
                       trade_date=trade_date,
                       fields='ts_code,'
                              'trade_date,'
                              'close,'
                              'open,'
                              'high,'
                              'low,'
                              'pre_close,'
                              'change,'
                              'pct_chg,'
                              'vol,'
                              'amount')
        return df

    def getAllIndexDailyIndicatorByDate(self, trade_date):
        """
        根据日期获取大盘指数的每日指标
        :param trade_date: 日期, 格式: 20200202
        :return: 每日指标df, 出错返回None
        """
        df = funcRetry(self.pro.index_dailybasic, self.retry, self.intv,
                       trade_date=trade_date,
                       fields='ts_code,'
                              'trade_date,'
                              'total_mv,'
                              'float_mv,'
                              'total_share,'
                              'float_share,'
                              'free_share,'
                              'turnover_rate,'
                              'turnover_rate_f,'
                              'pe,'
                              'pe_ttm,'
                              'pb')
        return df

    def getSignalIndexDailyIndicatorByDate(self, stock_code, start_date, end_date):
        """
        根据日期获取大盘指数的每日指标
        :param end_date:
        :param start_date:
        :param stock_code:
        :return: 每日指标df, 出错返回None
        """
        df = funcRetry(self.pro.index_dailybasic, self.retry, self.intv,
                       ts_code=stock_code,
                       start_date=start_date,
                       end_date=end_date,
                       fields='ts_code,'
                              'trade_date,'
                              'total_mv,'
                              'float_mv,'
                              'total_share,'
                              'float_share,'
                              'free_share,'
                              'turnover_rate,'
                              'turnover_rate_f,'
                              'pe,'
                              'pe_ttm,'
                              'pb')
        return df

    def getSWClassify(self, level):
        """
        获取申万L1、L2、L3的分类数据
        :param level: str, L1、L2、L3
        :return: 分类df, 出错返回None
        """
        df = funcRetry(self.pro.index_classify, self.retry, self.intv,
                       level=level,
                       src='SW',
                       fields='index_code,industry_name,level,industry_code,src')
        return df

    def getStockSWIndustry(self, stock_code):
        """
        查询某只股票的申万行业信息
        :param stock_code: 股票代码, 例如: 000001.SZ
        :return: 行业信息df, 出错返回None
        """
        df = funcRetry(self.pro.index_member, self.retry, self.intv, ts_code=stock_code,
                       fields='index_code,index_name,con_code,con_name,in_date,out_date,is_new')
        return df

    # TODO:
    def getIndexSWIndustry(self, index_code):
        """
        根据申万的行业分类, 获取所有所属成分股
        :param index_code: 申万行业分类代码, 例如: 801020.SI
        :return: 成分股df, 出错返回None
        """
        df = funcRetry(self.pro.index_member, self.retry, self.intv, index_code=index_code,
                       fields='index_code,index_name,con_code,con_name,in_date,out_date,is_new')
        return df

    def getTradeSummaryByDate(self, trade_date):
        """
        获取指定日期各交易所的交易汇总信息
        :param trade_date: 日期, 格式: 20200202
        :return: 交易汇总df, 出错返回None
        """
        df = funcRetry(self.pro.daily_info, self.retry, self.intv,
                       trade_date=trade_date,
                       exchange='SZ,SH',
                       fields='trade_date,'
                              'ts_code,'
                              'ts_name,'
                              'com_count,'
                              'total_share,'
                              'float_share,'
                              'total_mv,'
                              'float_mv,'
                              'amount,'
                              'vol,'
                              'trans_count,'
                              'pe,'
                              'tr,'
                              'exchange')
        return df

    def getTradeSummaryByDateRange(self, start_date, end_date):
        """
        获取指定日期各交易所的交易汇总信息
        :param end_date:
        :param start_date:
        :return: 交易汇总df, 出错返回None
        """
        df = funcRetry(self.pro.daily_info, self.retry, self.intv,
                       start_date=start_date,
                       end_date=end_date,
                       exchange='SZ,SH',
                       fields='trade_date,'
                              'ts_code,'
                              'ts_name,'
                              'com_count,'
                              'total_share,'
                              'float_share,'
                              'total_mv,'
                              'float_mv,'
                              'amount,'
                              'vol,'
                              'trans_count,'
                              'pe,'
                              'tr,'
                              'exchange')
        return df

    def methods(self):
        return list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)), dir(self)))


if __name__ == '__main__':
    api = tusApi(MYTOKEN)
    print(api.getSignalIndexDailyIndicatorByDate('000001.SH', '20100101', '20200414'))
    exit()
    print(api.getSignalStockBalanceSheetByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalStockCashflowByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalStockLimitPriceByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getAllStockTradeCalendarByDate('20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalStockProfitByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalStockExpressNewsByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalStockFinanceIndicatorByDate('000001.SZ', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalIndexDailyQuantByDate('000001.SH', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalIndexWeeklyQuantByDate('000001.SH', '20100101', '20200414'))
    time.sleep(2)
    print(api.getSignalIndexMonthlyQuantByDate('000001.SH', '20100101', '20200414'))
    time.sleep(2)
