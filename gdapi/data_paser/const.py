
# *****************************证券业务数据结构开始**************************
# 外网运营商
WAN_TC = 0  # 电信
WAN_NC = 1  # 网通
WAN_UC = 2  # 联通
WAN_MC = 3  # 移动
WAN_CC = 4  # 广电

# 订阅方式 v
RSS_MODE_NEW = 0  # 最新订阅
RSS_MODE_INC = 1  # 增量订阅

# 订阅推送位置
UI_RSS_POSSTART = 0  # 订阅推送位置从最开始
UI_RSS_POSCUR = 0XFFFFFFFF  # 订阅推送位置从当前

# 错误源定义,cb_ErrMsg回调中使用
ERRMSGSRC_CONNECT = 0x81  # 连接
ERRMSGSRC_LOGIN = 0x82  # 登录
ERRMSGSRC_MARKETSTATE = 0x83  # 市场状态

# 市场状态定义
MARKET_STATE_BREAK = 1  # 休市
MARKET_STATE_CLOSE = 2  # 闭市

# 登录方式
UI_LOGIN_NORMAL = 0x81  # 普通模式
UI_LOGIN_UPLINK = 1  # 级联模式
UI_LOGIN_PGM = 2  # PGM模式

# 网络模式
SIP_SVR_WAN = 0  # SIP_SVR的外网IP
SIP_SVR_LAN = 1  # SIP_SVR的内网IP

# 代理类型
TCP_PROXY_NONE = 0  # 不使用代理SOCKET5
TCP_PROXY_SOCKET5 = 1  # SOCKET5代理
TCP_PROXY_HTTP = 2  # 暂不支持

errorStringList = [
    " 成功",  # 0x00
    " 未知错误",  # 0x01
    " 无效句柄",  # 0x02
    " 参数错误",  # 0x03
    " 错误的数据或数据无效",  # 0x04
    " 错误的表达式",  # 0x05
    "",  # 0x06
    " 报文错误",  # 0x07
    " 未初始化",  # 0x08
    "",  # 0x09
    "",  # 0x0a
    "",  # 0x0b
    "",  # 0x0c
    "",  # 0x0d
    "",  # 0x0e
    " 不支持的命令",  # 0x0F
    " 网络未连接",  # 0x10
    " 网络超时",  # 0x11
    " 服务器连接满",  # 0x12
    " 网络错误",  # 0x13
    "",  # 0x14
    "",  # 0x15
    "",  # 0x16
    "",  # 0x17
    "",  # 0x18
    "",  # 0x19
    "",  # 0x1a
    "",  # 0x1b
    "",  # 0x1c
    "",  # 0x1d
    "",  # 0x1e
    "",  # 0x1F
    " 无此用户",  # 0x20
    " 无此权限",  # 0x21
    " 帐号不活动",  # 0x22
    " 密码错误",  # 0x23
    "",  # 0x24
    "",  # 0x25
    "",  # 0x26
    "",  # 0x27
    "",  # 0x28
    "",  # 0x29
    "",  # 0x2a
    "",  # 0x2b
    "",  # 0x2c
    "",  # 0x2d
    "",  # 0x2e
    "",  # 0x2f
    " 主键不存在",  # 0x30
    " 主键已经存在",  # 0x31
    " 没有定义错的抽象数据类型",  # 0x32
    "",  # 0x33
    "",  # 0x34
    "",  # 0x35
    "",  # 0x36
    "",  # 0x37
    "",  # 0x38
    "",  # 0x39
    "",  # 0x3a
    "",  # 0x3b
    "",  # 0x3c
    "",  # 0x3d
    "",  # 0x3e
    "",  # 0x3f
    " 订阅满",  # 0x40
    " 没有订阅",  # 0x41
    " info_svr没有运行或者连接失败!",  # 0x42
    " 用户已达到最大同时登录数，不能再连接",  # 0x43
    " IP被屏蔽",  # 0x44
    " 版本错误",  # 0x45
    " 不容许级联",  # 0x46
    " 加入可靠多播错误",  # 0x47
    " 接收缓冲溢出",  # 0x48
    " 无PGM读取权限",  # 0x49
    "",  # 0x4a
    "",  # 0x4b
    "",  # 0x4c
    "",  # 0x4d
    "",  # 0x4e
    "",  # 0x4f
    "",  # 0x50
    " UI库错误",  # 0x51
    " MI库错误",  # 0x52
    " 没有服务器，动态连接时，当没有sip_svr运行时会返回这个错误代码.",  # 0x53
    " 无此市场",  # 0x54
    " 无此编码，当不能转换为抽象ID时，返回此错误",  # 0x55
    " 用户名非数字格式",  # 0x56
    " 超出最大用户数,TDR_SubscribeTrand可能会返回这个错误",  # 0x57
    " 没有快照，是指创建时不使用快照，Get接口会返回这个错误码",  # 0x58
    " 库错误，一般是没有找到库或者使用了错误的库",  # 0x59
]

# *****************************证券业务数据结构结束**************************



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 上海证券交易所 **********************************
HQD_MARKET_SH = 1
ID_SH_INDEXDATA = 0x00  # 指数(Stock_IndexData)
ID_SH_TRANSACTION = 0x01  # 成交(Stock_Transaction)
ID_SH_ORDERQUEUE = 0x02  # 委托队列(Stock_OrderQueue_Head+Stock_OrderQueue)
ID_SH_MARKETDATA = 0x04  # 行情数据(Stock_MarketData)
ID_SH_MARKETDATA_L1 = 0x05  # 用于L1行情 上海(Stock_MarketData_L1)
ID_SH_KLINEDATA = 0x07  # 上交所个股分钟K线数据(T_SH_Kline)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 深圳证券交易所 **********************************
HQD_MARKET_SZ = 2
ID_SZ_INDEXDATA = 0x00  # 指数(Stock_IndexData)
ID_SZ_TRANSACTION = 0x01  # 成交(Stock_TransactionEx)
ID_SZ_ORDERQUEUE = 0x02  # 委托队列(Stock_OrderQueue_Head+Stock_OrderQueue)
ID_SZ_STEPORDER = 0x03  # 逐笔委托(Stock_StepOrder)
ID_SZ_MARKETDATA = 0x04  # 行情数据(Stock_MarketData)
ID_SZ_MARKETDATA_L1 = 0x06  # 用于V5 L1行情 深圳(Stock_MarketData_L1)
ID_SZ_KLINEDATA = 0x07  # 深交所个股分钟K线数据(T_SZ_Kline)
ID_SZ_QDHQDATA = 0x08  # 深交所千档行情数据(t_SZ_QDHQData)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 中金所 **********************************
HQD_MARKET_CFFEX = 3
ID_CFFEX_MARKETDATA = 0x01  # 期货及期权行情数据(Futures_MarketData)
ID_CFFEX_BASEINFO = 0X02  # 期权及基权基础信息
ID_CFFEX_FORQOUTE = 0x03  # 询价通知

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 郑商所 **********************************
HQD_MARKET_CZCE = 4
ID_CZCE_MARKETDATA = 0x01  # 期货行情数据(Futures_MarketData)  1016
ID_CZCE_BASEINFO = 0x02  # 期货基础信息
ID_CZCE_FORQOUTE = 0x03  # 询价通知

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 大商所 **********************************
HQD_MARKET_DCE = 5
ID_DCE_MARKETDATA = 0x01  # 期货行情数据(Futures_MarketData)
ID_DCE_BASEINFO = 0x02  # 期货基础信息
ID_DCE_FORQOUTE = 0x03  # 询价通知

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 上期所 **********************************
HQD_MARKET_SHFE = 6
ID_SHFE_MARKETDATA = 0x01  # 期货行情数据(Futures_MarketData)
ID_SHFE_BASEINFO = 0x02  # 期货基础信息
ID_SHFE_FORQOUTE = 0x03  # 询价通知

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 中证指数行情市场 **********************************
HQD_MARKET_ZZZS = 7
ID_ZZZS_INDEX = 0x01  # 中证指数行情 对应T_ZZZS_IndexMarketData
ID_ZZZS_WEIGHT = 0x02  # 权重信息 对应T_ZZZS_IndexWeight
ID_ZZZS_ETFIOPV = 0x03  # ETF的IOPV 对应T_ZZZS_EtfIopv

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 中证指数行情市场 **********************************
HQD_MARKET_SHOP = 8  # 上交所期权
ID_SHOP_BASEINFO = 0x01  # 期权基础信息 对应T_SH_OptionBaseInfo
ID_SHOP_MARKETDATA = 0x02  # 期权市场代码 对应T_SH_OptionMarketData

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 香港市场 **********************************
HQD_MARKET_HK = 9  #
ID_HK_ORGMSG = 1  # 原始OMD消息数据，需要开启内存存储，每个证券至少2个页面
ID_HK_EXMSG = 2  # 扩展消息，10档行情，目前只有 消息号为90 的消息(10档行情),如果大于一个，也需要开启内存存储
ID_HK_CUR = 3  # 汇率 对应omd 14
ID_HK_INDEX = 4  # 指数 对应omd 71
ID_HK_BASEINFO = 5  # 基础信息 对应omd 11
ID_HK_COUNT = 6  # 统计  对应 omd 60
ID_HK_CLOSEPRICE = 7  # 收盘价 对应 omd 62
ID_HK_EXMSGL1 = 8  # 扩展消息 消息号91 5档行情

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 深交所期权 **********************************
HQD_MARKET_SZOP = 11
ID_SZOP_BASEINFO = 1  # 期权基础信息
ID_SZOP_MARKETDATA = 2  # 期权快照行情

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 上海黄金市场 **********************************
HQD_MARKET_SGE = 12
ID_SGE_MARKETDATA = 0x01  # 市场数据(t_SGE_MarketData)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 香港市场 **********************************
HQD_MARKET_SHHK = 13
ID_SHHK_INDEX = 0x00  # 指数(Stock_Index)
ID_SHHK_SNAPSHOT = 0x01  # 快照(Stock_Snapshot)
ID_SHHK_TRADETICK = 0x02  # 分笔成交(Stock_TradeTick)
ID_SHHK_ODDLOT = 0x03  # 碎骨订单(Stock_OddLot)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 新三板市场 **********************************
HQD_MARKET_NEEQ = 15
ID_NEEQ_INDEXDATA = 0x00  # 指数数据(Stock_IndexData)
ID_NEEQ_MARKETDATA = 0x01  # 行情数据(Stock_MarketData)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ********************************* 静态资讯 **********************************
HQD_MARKET_JTZX = 16
ID_JTZX_COMPASHAREINFO = 0x00  # 上市公司概况(t_JTZX_CompAShareInfo)
ID_JTZX_HOLDERINFO = 0x01  # 股东信息(t_JTZX_HolderInfo)
ID_JTZX_FININDEX = 0x02  # 财务指标(t_JTZX_FinIndex)
ID_JTZX_MAINBUSINESS = 0x03  # 主营构成(t_JTZX_MainBusiness)
ID_JTZX_ANNOUNCEMENT = 0x04  # 近期公告(t_JTZX_Announcement)
ID_JTZX_RANKLIST = 0x05  # 龙虎榜(t_JTZX_Ranklist)
ID_JTZX_BLOCKTRADE = 0x06  # 大宗交易(t_JTZX_BlockTrade)
ID_JTZX_MARGINTRADE = 0x07  # 融资融券(t_JTZX_MarginTrade)
