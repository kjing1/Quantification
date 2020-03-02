from gdapi.data_paser.const import *
from gdapi.data_paser.ctypes_utils import *


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 数据解析函数 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ------------------------------------- 沪深市场 ------------------------------------

# ***************************** Level2 ： 沪深交易所 ****************************** #
def StockMarketDataL2(stream, l, market):
    if market not in (HQD_MARKET_SH, HQD_MARKET_SZ):
        raise AttributeError('MARKET ERROR FOR LEVEL2')
        return None
    mds = []
    SIZE_OF_MDL2 = 264
    size = int(l / SIZE_OF_MDL2)
    for i in range(0, size):
        ms = {'type': 'Level2'}
        ms['nTime'] = stream.Read32()  # 时间(HHMMSSmmmm)
        ms['nStatus'] = stream.Read32()  # 状态
        ms['uPreClose'] = stream.Read32()  # 前收盘价
        ms['uOpen'] = stream.Read32()  # 开盘价
        ms['uHigh'] = stream.Read32()  # 最高价
        ms['uLow'] = stream.Read32()  # 最低价
        ms['uMatch'] = stream.Read32()  # 最新价

        uAskPrice = []
        uAskVol = []
        uBidPrice = []
        uBidVol = []
        for x in range(0, 10): uAskPrice.append(stream.Read32())
        for x in range(0, 10): uAskVol.append(stream.Read32())
        for x in range(0, 10): uBidPrice.append(stream.Read32())
        for x in range(0, 10): uBidVol.append(stream.Read32())

        ms['uAskPrice'] = uAskPrice  # 申卖价
        ms['uAskVol'] = uAskVol  # 申卖量
        ms['uBidPrice'] = uBidPrice  # 申买价
        ms['uBidVol'] = uBidVol  # 申买量
        ms['uNumTrades'] = stream.Read32()  # 成交笔数
        ms['iVolume'] = stream.Read64()  # 成交总量
        ms['iTurnover'] = stream.Read64()  # 成交总金额
        ms['iTotalBidVol'] = stream.Read64()  # 委托买入总量
        ms['iTotalAskVol'] = stream.Read64()  # 委托卖出总量
        ms['uWeightedAvgBidPrice'] = stream.Read32()  # 加权平均委买价格
        ms['uWeightedAvgAskPrice'] = stream.Read32()  # 加权平均委卖价格
        ms['nIOPV'] = stream.Read32()  # IOPV净值估值
        ms['nYieldToMaturity'] = stream.Read32()  # 到期收益率
        ms['uHighLimited'] = stream.Read32()  # 涨停价
        ms['uLowLimited'] = stream.Read32()  # 跌停价
        ms['sPrefix'] = stream.ReadString(4)  # 证券信息前缀
        ms['nSyl1'] = stream.Read32()  # 市盈率1 2 位小数 股票：价格/上年每股利润 债券：每百元应计利息
        ms['nSyl2'] = stream.Read32()  # 市盈率2 2 位小数 股票：价格/本年每股利润 债券：到期收益率 基金：每百份的IOPV 或净值 权证：溢价率
        ms['nSD2'] = stream.Read32()  # 升跌2（对比上一笔）

        if market == HQD_MARKET_SH:
            ms['sTradingPhraseCode'] = stream.ReadString(
                8)  # 该字段为8位字符串，左起每位表示特定的含义，无定义则填空格。第1位：‘S’表示启动（开市前）时段，‘C’表示集合竞价时段，‘T’表示连续交易时段，‘B’表示休市时段，‘E’表示闭市时段，‘P’表示产品停牌。
            ms['nPreIOPV'] = stream.Read32()  # 基金 T-1 日收盘时刻 IOPV 仅标的为基金时有效

        mds.append(ms)
    return mds


# ***************************** 指数行情 ： 沪深交易所 ****************************** #
def StockIndexData(stream, l):
    indexes = []
    SIZE_OF_INDEX_DATA = 40
    size = int(l / SIZE_OF_INDEX_DATA)
    for i in range(0, size):
        index = {'type': 'Index'}
        index['nTime'] = stream.Read32()  # 时间(HHMMSSmmmm)
        index['nOpen'] = stream.Read32()  # 今开盘指数
        index['nHigh'] = stream.Read32()  # 最高指数
        index['nLow'] = stream.Read32()  # 最低指数
        index['nprice'] = stream.Read32()  # 最新指数
        index['iTotalVolume'] = stream.Read64()  # 参与计算相应指数的交易数量
        index['iTurnover'] = stream.Read64()  # 参与计算相应指数的成交金额
        index['nPreCloseIndex'] = stream.Read32()  # 前盘指数
        indexes.append(index)
    return indexes


# ***************************** 分钟K线 ： 沪深交易所 ****************************** #
def Kline(stream, l):
    klines = []
    size = int(l / 40)
    for i in range(0, size):
        kline = {'type': 'Kline'}
        kline['uDay'] = stream.Read32()  # 日期        YYYYMMDD
        kline['nTime'] = stream.Read32()  # 时间(北京时间)  HHMM
        kline['nPreClose'] = stream.Read32()  # 前收盘价         单位：1/100分
        kline['nValOpen'] = stream.Read32()  # 开盘价      单位：1/100分,比如1表示0.0001元
        kline['nValHigh'] = stream.Read32()  # 最高价      单位：1/100分
        kline['nValLow'] = stream.Read32()  # 最低价      单位：1/100分
        kline['nValClose'] = stream.Read32()  # 收盘价      单位：1/100分
        kline['i64Volume'] = stream.Read64()  # 分钟内成交量    单位：该证券的最小交易单位，比如股票为“股”
        kline['i64ValTotal'] = stream.Read64()  # 分钟内成交额    单位：元
        kline['i64TotalVol'] = stream.Read64()  # 累计成交量    单位：该证券的最小交易单位，比如股票为“股”
        kline['i64TotalTurnOver'] = stream.Read64()  # 累计成交金额    单位：元
        kline['nTurover'] = stream.Read32()  # 换手(百分数)    单位：1/10000，比如1表示0.01%
        kline['nValIncrease'] = stream.Read32()  # 涨跌值      单位：1/100分
        klines.append(kline)
    return klines


# ***************************** 订单（委托）队列 ： 沪深交易所 ****************************** #
def ParseOrderQueue(stream, size):
    oqs = []
    for x in range(0, int(size)):
        oq = {'type': 'OrderQueue'}
        oq['nTime'] = stream.Read32()       # 订单时间(HHMMSSmmmm)
        oq['nSide'] = stream.Read32()       # 买卖方向('B':Bid 'S':Ask)
        oq['nPrice'] = stream.Read32()      # 成交价格
        oq['nOrders'] = stream.Read32()     # 订单数量
        oq['nABItems'] = stream.Read32()    # 明细个数
        nABVolume = []
        for j in range(0, 200): nABVolume.append(stream.Read32())
        oq['nABVolume'] = nABVolume         # 订单明细
        oqs.append(oq)
    return oqs


def OrderQueue(stream):
    nItems = stream.Read32()
    return ParseOrderQueue(stream, nItems)


# ***************************** 逐笔成交 ： 上海交易所  ****************************** #
def SH_Transaction(stream, l):
    ts = []
    size = int(l / 52)
    for i in range(0, size):
        tran = {'type': 'SH_Transaction'}
        tran['nTradeIndex'] = stream.Read32()
        tran['nTradeChannel'] = stream.Read32()
        tran['nTradeTime'] = stream.Read32()
        tran['nTradePrice'] = stream.Read32()
        tran['iTradeQty'] = stream.Read64()
        tran['iTradeMoney'] = stream.Read64()
        tran['iTradeBuyNo'] = stream.Read64()
        tran['iTradeSellNo'] = stream.Read64()
        tran['cTradeBSflag'] = stream.ReadChar()
        tran['sRes'] = stream.ReadString(3)
        ts.append(tran)
    return ts


# ***************************** 逐笔成交 ： 深圳交易所  ****************************** #
def SZ_Transaction(stream, size):
    ts = []
    for x in range(0, int(size / 36)):
        t = {'type': 'SZ_Transaction'}
        t['uSetno'] = stream.Read32()           # 证券集代码
        t['nTradeIndex'] = stream.Read32()      # 成交索引 指定证券集上唯一记录标识 从1 开始计数
        t['iTradeBuyNo'] = stream.Read32()      # 买方委托索引 从1 开始计数，0 表示无对应委托
        t['iTradeSellNo'] = stream.Read32()     # 卖方委托索引 从1 开始计数，0 表示无对应委托
        t['nTradePrice'] = stream.Read32()      # 成交价格 扩大10000倍
        t['iTradeQty'] = stream.Read32()        # 成交数量
        t['cOrderKind'] = stream.ReadChar()     # 成交类别
        t['sResv1'] = stream.ReadString(3)      # 保留字段1
        t['cFunctionCode'] = stream.ReadChar()  # 成交代码
        t['sResv2'] = stream.ReadString(3)      # 保留字段2
        t['nTradeTime'] = stream.Read32()       # 成交时间
        ts.append(t)
    return ts


# ***************************** 逐笔委托 ： 仅深圳交易所  ****************************** #
def SZ_StockStepOrder(stream, l):
    sos = []
    size = int(l / 28)
    for x in range(0, size):
        so = {'type': 'SZ_StockStepOrder'}
        so['uSetno'] = stream.Read32()             # 证券集代码
        so['uRecno'] = stream.Read32()             # 成交索引 指定证券集上唯一记录标识 从1 开始计数
        so['uPrice'] = stream.Read32()             # 委托编号
        so['uOrderQty'] = stream.Read32()          # 委托价格
        so['cOrderKind'] = stream.ReadChar()       # 成交类别
        so['sResv1'] = stream.ReadString(3)        # 保留字段1
        so['cFunctionCode'] = stream.ReadChar()    # 成交代码
        so['sResv2'] = stream.ReadString(3)        # 保留字段2
        so['nOrderEntryTime'] = stream.Read32()    # 委托时间
        sos.append(so)
    return sos


# ***************************** 千档行情 ： 仅深圳交易所  ****************************** #
# 待定义
def SZ_QDHQ(stream, l):
    qd = []
    size = int(l / 192)
    for i in range(0, size):
        qdhq = {'type': 'SZ_QDHQ'}
        qdhq['nTime'] = stream.Read32()             # 时间(HHMMSSmmmm)
        qdhq['uMatch'] = stream.Read32()            # 最新价
        uAskPrice = []
        uAskVol = []
        uBidPrice = []
        uBidVol = []
        for x in range(0, 10): uAskPrice.append(stream.Read32())
        for x in range(0, 10): uAskVol.append(stream.Read32())
        for x in range(0, 10): uBidPrice.append(stream.Read32())
        for x in range(0, 10): uBidVol.append(stream.Read32())
        qdhq['uAskPrice'] = uAskPrice               # 申卖价
        qdhq['uAskVol'] = uAskVol                   # 申卖量
        qdhq['uBidPrice'] = uBidPrice               # 申买价
        qdhq['uBidVol'] = uBidVol                   # 申买量
        qdhq['iTotalBidAmount'] = stream.Read64()  # 总买量
        qdhq['iTotalAskAmount'] = stream.Read64()  # 总卖量
        qdhq['iTotalVolume'] = stream.Read64()     # 总成交量

        qd.append(qdhq)
    return qd
# -----------------------------------------------------------其他市场-------------------------------
# ***************************** 期货行情 ： 四大期货交易所  ****************************** #
def Market_Future(stream, size):
    mfs = []
    for i in range(0, int(size)):
        mf = {'type': 'Option'}
        mf['nTime'] = stream.Read32()
        mf['nStatus'] = stream.Read32()
        mf['iPreOpenInterest'] = stream.Read64()
        mf['uPreClose'] = stream.Read32()
        mf['uPreSettlePrice'] = stream.Read32()
        mf['uOpen'] = stream.Read32()
        mf['uHigh'] = stream.Read32()
        mf['uLow'] = stream.Read32()
        mf['uMatch'] = stream.Read32()
        mf['iVolume'] = stream.Read64()
        mf['iTurnover'] = stream.Read64()
        mf['iOpenInterest'] = stream.Read64()
        mf['uClose'] = stream.Read32()
        mf['uSettlePrice'] = stream.Read32()
        mf['uHighLimited'] = stream.Read32()
        mf['uLowLimited'] = stream.Read32()
        mf['nPreDelta'] = stream.Read32()
        mf['nCurrDelta'] = stream.Read32()

        uAskPrice = []
        uAskVol = []
        uBidPrice = []
        uBidVol = []
        for x in range(0, 5): uAskPrice.append(stream.Read32())
        for x in range(0, 5): uAskVol.append(stream.Read32())
        for x in range(0, 5): uBidPrice.append(stream.Read32())
        for x in range(0, 5): uBidVol.append(stream.Read32())

        mf['uAskVol'] = uAskVol
        mf['uBidPrice'] = uBidPrice
        mf['uAskPrice'] = uAskPrice
        mf['uBidVol'] = uBidVol
        mfs.append(mf)
    return mfs


# ***************************** 期权行情 ： 上海交易所  ****************************** #
def SHOP_MarketData(stream, size):
    smds = []
    for i in range(0, int(size)):
        smd = {'type': 'SHOP_MarketData'}
        smd['nDataTimestamp'] = stream.Read32()
        smd['iPreSettlPrice'] = stream.Read64()
        smd['iSettlPrice'] = stream.Read64()
        smd['iOpenPx'] = stream.Read64()
        smd['iHighPx'] = stream.Read64()
        smd['iLowPx'] = stream.Read64()
        smd['iLastPx'] = stream.Read64()
        smd['iAuctionPrice'] = stream.Read64()
        smd['iAuctionQty'] = stream.Read64()
        smd['iTotalLongPosition'] = stream.Read64()
        iBidSize = []
        iBidPx = []
        iOfferSize = []
        iOfferPx = []
        for x in range(0, 5): iBidSize.append(stream.Read64())
        for x in range(0, 5): iBidPx.append(stream.Read64())
        for x in range(0, 5): iOfferSize.append(stream.Read64())
        for x in range(0, 5): iOfferPx.append(stream.Read64())

        smd['iBidSize'] = iBidSize
        smd['iBidPx'] = iBidPx
        smd['iOfferSize'] = iOfferSize
        smd['iOfferPx'] = iOfferPx
        smd['iTotalVolumeTrade'] = stream.Read64()
        smd['iTotalValueTrade'] = stream.Read64()
        smd['sTradingPhaseCode'] = stream.ReadString(5)
        smds.append(smd)
    return smds

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%% 根据 MarkeCode、ServiceID 解析数据 %%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# 上海市场
def Market_SH(serviceId, stream, length):
    if serviceId == ID_SH_INDEXDATA:
        return StockIndexData(stream, length)  # 指数
    elif serviceId == ID_SH_TRANSACTION:
        return SH_Transaction(stream, length)  # 逐笔成交
    elif serviceId == ID_SH_ORDERQUEUE:
        return OrderQueue(stream)  # 委托队列
    elif serviceId == ID_SH_MARKETDATA:  # L2行情数据
        return StockMarketDataL2(stream, length, HQD_MARKET_SH)
    elif serviceId == ID_SH_KLINEDATA:
        return Kline(stream, length)  # 个股分钟K线
    else:
        raise AttributeError('SH SERVICEID ERROR')


# 深圳市场
def Market_SZ(serviceId, stream, length):
    if serviceId == ID_SZ_INDEXDATA:
        return StockIndexData(stream, length)  # 指数
    elif serviceId == ID_SZ_ORDERQUEUE:
        return OrderQueue(stream)  # 沪深订单（委托）队列数据结构一致
    elif serviceId == ID_SZ_TRANSACTION:
        return SZ_Transaction(stream, length)  # 逐笔成交
    elif serviceId == ID_SZ_MARKETDATA:
        return StockMarketDataL2(stream, length, HQD_MARKET_SZ)  # 沪深l2行情数据结构一致
    elif serviceId == ID_SZ_KLINEDATA:
        return Kline(stream, length)  # 个股分钟K线
    elif serviceId == ID_SZ_STEPORDER:
        return SZ_StockStepOrder(stream, length)  # 逐笔委托
    elif serviceId == ID_SZ_QDHQDATA:
        serviceId = serviceId
        return SZ_QDHQ(stream, length)            # 千档行情

    else:
        raise AttributeError('SZ SERVICEID ERROR')


# 入口函数
def FromMdarec(market, serviceID, stream, length):
    pdata_offset = 0
    pData = None
    if market == HQD_MARKET_SH:
        pData = Market_SH(serviceID, Stream(stream[pdata_offset:length]), length)
    elif market == HQD_MARKET_SZ:
        pData = Market_SZ(serviceID, Stream(stream[pdata_offset:length]), length)
    elif 3 <= market <= 6:
        SIZE_OF_FUTURE = 168
        future_size = length / SIZE_OF_FUTURE
        pData = Market_Future(Stream(stream[pdata_offset:length]), int(future_size))
    elif market == HQD_MARKET_SH:
        SIZE_OF_SHOP_MarketData = 257
        shop_size = length / SIZE_OF_SHOP_MarketData
        pData = SHOP_MarketData(Stream(stream[pdata_offset:length]), int(shop_size))
    else:
        print("error, unknow market code")
    return pData
