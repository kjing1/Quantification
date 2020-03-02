# python 3.7.4
# coding = utf-8
# filename api.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import ctypes
from gdapi.data_paser.parser_functions import FromMdarec
from gdapi.data_paser.const import *
from pprint import pprint
import time
import os
import log

LOGGER = log.init_logging('.\\gdlog.txt', 'debug')


def set_OnReceiveData(pUserParam, nDate, nMarketId, sCode, sName, uType, nServiceId, pData, nLen):
    """
    光大接口数据回调函数
    void  __stdcall OnReceiveData(
        void* pUserParam,   # [in]用户自定义参数,由用户调用TDR_Create时传入
        T_I32 nDate,        # [in]日期
        T_I32 nMarketId,    # [in]市场代码，参见tdr.h中对市场进行的宏定义
        const char* sCode,  # [in]证券代码
        const char* sName,  # [in]证券名称
        T_U32 uType,        # [in]证券类型
        T_I32 nServiceId,   # [in]服务数据ID，比如行情、逐笔成交等，参见tdr.h文件定义
        void* pData,        # [in]数据内容
        T_I32 nLen          # [in]数据长度
        )
    """
    LOGGER.debug('TRIGGERED with param(pUserParam:%s, nDate:%s, nMarketId:%s, sCode:%s, sName:%s, uType:%s, '
                 'nServiceId:%s, pData:%s, nLen:%s)' % (
                     pUserParam, nDate, nMarketId, sCode, sName, uType, nServiceId, pData, nLen))
    g = (ctypes.c_char * nLen).from_address(pData)
    ret_mds = FromMdarec(nMarketId, nServiceId, g[0:nLen], nLen)
    LOGGER.info('get all %d datas' % len(ret_mds))
    if len(ret_mds) > 0:    pprint(ret_mds[0])


# 注册数据回调C函数
ONRECEIVEDATAFUNC = ctypes.CFUNCTYPE(None,
                                     ctypes.c_void_p,
                                     ctypes.c_int,
                                     ctypes.c_int,
                                     ctypes.c_char_p,
                                     ctypes.c_char_p,
                                     ctypes.c_uint,
                                     ctypes.c_int,
                                     ctypes.c_void_p,
                                     ctypes.c_int)
callback_OnReceiveData = ONRECEIVEDATAFUNC(set_OnReceiveData)


def set_OnErrorMsg(pUserParam, nError, nErrSource, uData):
    """
    光大接口错误回调函数
    :param LOGGER: 日志对象
    :param pUserParam: see set_OnReceiveData
    :param nError: see set_OnReceiveData
    :param nErrSource: see set_OnReceiveData
    :param uData: see set_OnReceiveData
    :return:
    """
    LOGGER.debug('TRIGGERED with param(pUserParam:%s, nError:%s, nErrSource:%s, uData:%s)' % (
        pUserParam, nError, nErrSource, uData))
    if nError == 0 and nErrSource == ERRMSGSRC_LOGIN:
        LOGGER.debug('%d-%s' % (nError, errorStringList[nError]))
    else:
        if nErrSource == ERRMSGSRC_MARKETSTATE and nError in (
                HQD_MARKET_SH, HQD_MARKET_SZ) and uData == MARKET_STATE_CLOSE:
            LOGGER.error('Market closed %d' % nError)
        else:
            LOGGER.error('Unkown error: %d' % nError)


# 注册错误回调C函数
ONERRORMSGFUNC = ctypes.CFUNCTYPE(None,
                                  ctypes.c_void_p,
                                  ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_uint)
callback_OnErrorMsg = ONERRORMSGFUNC(set_OnErrorMsg)


def init_inst(dlldir, dllpath):
    """
    打开库文件并创建可执行句柄
    :param dlldir: 光大库文件目录
    :param dllpath: 要打开的库文件路径
    :return: dll + 句柄
    """
    if not os.path.exists(os.path.expanduser(dllpath)) or \
            not os.path.exists(os.path.expanduser(dlldir)):
        LOGGER.error('%s or %s not exist' % (dlldir, dllpath))
        return None, None
    os.environ['PATH'] = os.path.expanduser(dlldir) + ';' + os.environ['PATH']
    inst = ctypes.windll.LoadLibrary(os.path.expanduser(dllpath))
    inst.TDR_Create.restype = ctypes.c_int64
    inst.TDR_Create.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                ctypes.c_bool, ctypes.c_bool]
    handle = inst.TDR_Create(ctypes.c_char_p(0),
                             callback_OnReceiveData,
                             ctypes.c_void_p(0),
                             callback_OnErrorMsg,
                             ctypes.c_void_p(0),
                             ctypes.c_bool(True),
                             ctypes.c_bool(True))
    return inst, handle


def gd_login(inst, handle, uesrname, password, serverip, port, nettype, netoperator, loginmode, timeout):
    """
    登录到光大接口
    :param inst: init_inst()返回的inst
    :param handle: init_inst()返回的handle
    :param uesrname: 光大接口用户名
    :param password: 光大接口用户密码
    :param serverip: 服务器IP
    :param port: 服务器端口
    :param nettype: 网络模式：
                            SIP_SVR_WAN = 0  # SIP_SVR的外网
                            IPSIP_SVR_LAN = 1  # SIP_SVR的内网IP
    :param netoperator: 网络运营商：
                            WAN_TC = 0  # 电信
                            WAN_NC = 1  # 网通
                            WAN_UC = 2  # 联通
                            WAN_MC = 3  # 移动
                            WAN_CC = 4  # 广电
    :param loginmode: 登录模式：
                            UI_LOGIN_NORMAL = 0x81  # 普通模式，登陆后用户需主动订阅，触发注册的回调函数
                            UI_LOGIN_UPLINK = 1  # 级联模式，则无需订阅，登陆后自动获取全部行情 并触发注册的回调函数
                            UI_LOGIN_PGM = 2  # PGM模式
    :param timeout: 超市时间（秒）
    :return:
    """
    inst.TDR_ConnectByDynamic.restype = ctypes.c_int64
    inst.TDR_ConnectByDynamic.argtypes = [ctypes.c_int64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                          ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
    ret = inst.TDR_ConnectByDynamic(handle,
                                    ctypes.c_char_p(serverip.encode('utf-8')),
                                    ctypes.c_int(port),
                                    ctypes.c_int(nettype),
                                    ctypes.c_int(netoperator),
                                    ctypes.c_char_p(uesrname.encode('utf-8')),
                                    ctypes.c_char_p(password.encode('utf-8')),
                                    ctypes.c_int(loginmode),
                                    ctypes.c_int(timeout))
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    return ret


def gd_subscribe(inst, handle, mcode, scode, mode, serviceid):
    """
    通过证券代码订阅实时行情
    :param inst: dll句柄
    :param handle: 光大库句柄
    :param mcode: 市场代码
                    HQD_MARKET_SH = 1 # 上海交易所
                    HQD_MARKET_SZ = 2 # 深圳交易所
                    HQD_MARKET_CFFEX = 3 # 中金所
                    HQD_MARKET_CZCE = 4 # 郑商所
                    HQD_MARKET_DCE = 5 # 大商所
                    HQD_MARKET_SHFE = 6 # 上期所
                    HQD_MARKET_ZZZS = 7 # 中证指数行情市场
                    HQD_MARKET_SHOP = 8  # 上交所期权
                    HQD_MARKET_HK = 9  # 香港市场
                    HQD_MARKET_SZOP = 11 # 深交所期权
                    HQD_MARKET_SGE = 12 # 上海黄金市场
                    HQD_MARKET_SHHK = 13 # 香港市场？
                    HQD_MARKET_NEEQ = 15 # 新三板市场
                    HQD_MARKET_JTZX = 16 # 静态咨询
    :param scode: 证券代码
    :param mode: 订阅模式
                    RSS_MODE_NEW = 0  # 最新订阅
                    RSS_MODE_INC = 1  # 增量订阅
    :param serviceid: 服务编码
                    HQD_MARKET_SH = 1 # 上海交易所
                        ID_SH_INDEXDATA = 0x00  # 指数(Stock_IndexData)
                        ID_SH_TRANSACTION = 0x01  # 成交(Stock_Transaction)
                        ID_SH_ORDERQUEUE = 0x02  # 委托队列(Stock_OrderQueue_Head+Stock_OrderQueue)
                        ID_SH_MARKETDATA = 0x04  # 行情数据(Stock_MarketData)
                        ID_SH_MARKETDATA_L1 = 0x05  # 用于L1行情 上海(Stock_MarketData_L1)
                        ID_SH_KLINEDATA = 0x07  # 上交所个股分钟K线数据(T_SH_Kline)
                    HQD_MARKET_SZ = 2
                        ID_SZ_INDEXDATA = 0x00  # 指数(Stock_IndexData)
                        ID_SZ_TRANSACTION = 0x01  # 成交(Stock_TransactionEx)
                        ID_SZ_ORDERQUEUE = 0x02  # 委托队列(Stock_OrderQueue_Head+Stock_OrderQueue)
                        ID_SZ_STEPORDER = 0x03  # 逐笔委托(Stock_StepOrder)
                        ID_SZ_MARKETDATA = 0x04  # 行情数据(Stock_MarketData)
                        ID_SZ_MARKETDATA_L1 = 0x06  # 用于V5 L1行情 深圳(Stock_MarketData_L1)
                        ID_SZ_KLINEDATA = 0x07  # 深交所个股分钟K线数据(T_SZ_Kline)
                        ID_SZ_QDHQDATA = 0x08  # 深交所千档行情数据(t_SZ_QDHQData)
    :return: 0 - 成功，其他 - 失败
    """
    inst.TDR_SubscribeByCode.restypes = ctypes.c_int
    inst.TDR_SubscribeByCode.argtypes = [ctypes.c_int64,
                                         ctypes.c_char_p,
                                         ctypes.c_char_p,
                                         ctypes.c_int,
                                         ctypes.c_int]
    ret = inst.TDR_SubscribeByCode(handle, mcode, scode, mode, serviceid)
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    return ret


def gd_getdata(inst, handle, mcode, scode, serviceid, pdata, datalen):
    inst.TDR_GetMarketData.restypes = ctypes.c_int
    inst.TDR_GetMarketData.argtypes = [ctypes.c_int64,
                                       ctypes.c_char_p,
                                       ctypes.c_char_p,
                                       ctypes.c_int,
                                       ctypes.c_void_p,
                                       ctypes.c_int]
    ret = inst.TDR_GetMarketData(handle, mcode, scode, serviceid, pdata, datalen)
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    if ret == 0:
        print(pdata)
    return ret


def gd_unsubscribe(inst, handle):
    inst.TDR_UnsubscribeAll.restypes = ctypes.c_int
    inst.TDR_UnsubscribeAll.argtypes = [ctypes.c_int64]
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    return ret


def gd_isconnected(inst, handle):
    inst.TDR_IsConnected.restype = ctypes.c_bool
    inst.TDR_IsConnected.argtypes = [ctypes.c_int64]
    ret = inst.TDR_IsConnected(handle)
    LOGGER.info('Isconnencted? ret=%d' % ret)
    return ret


def gd_disconnect(inst, handle):
    inst.TDR_DisConnect.restype = ctypes.c_int
    inst.TDR_DisConnect.argtypes = [ctypes.c_int64]
    ret = inst.TDR_DisConnect(handle)
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    return ret


def gd_distroy(inst, handle):
    inst.TDR_Destroy.restypes = ctypes.c_int
    inst.TDR_Destroy.argtypes = [ctypes.c_int64]
    ret = inst.TDR_Destroy(handle)
    LOGGER.info('ret=%s，信息：%s' % (ret, errorStringList[ret]))
    return ret


DLLDIR = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\gdapi\\dll'
DLLPATH = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\gdapi\\dll\\sipuicom64.dll'
SERVER = '116.236.247.183'
PORT = 9888
USER = 'gdzq_jinshi'
PWD = 'test123456'


if __name__ == '__main__':
    dll, handle = init_inst(DLLDIR, DLLPATH)
    if dll is None or handle is None:
        print('Cannot load dll from: %s' % DLLPATH)

    ret = gd_login(dll, handle, USER, PWD, SERVER, PORT,
                   SIP_SVR_WAN, WAN_TC, UI_LOGIN_NORMAL, 15)
    print('Login: %d-%s' % (ret, errorStringList[ret]))

    ret = gd_subscribe(dll, handle, 'SH'.encode('utf-8'), '600000'.encode('utf-8'), RSS_MODE_INC, ID_SH_TRANSACTION)
    print('Subscribe: %d-%s' % (ret, errorStringList[ret]))

    while True:
        if gd_isconnected(dll, handle):
            print('Connected, wait TRANSACTIONS...')
            time.sleep(120)
        else:
            break

    ret = gd_unsubscribe(dll, handle)
    print('Unsubscribe: %d-%s' % (ret, errorStringList[ret]))

    ret = gd_disconnect(dll, handle)
    print('Disconnect: %d-%s' % (ret, errorStringList[ret]))

    ret = gd_distroy(dll, handle)
    print('Distroy: %d-%s' % (ret, errorStringList[ret]))
