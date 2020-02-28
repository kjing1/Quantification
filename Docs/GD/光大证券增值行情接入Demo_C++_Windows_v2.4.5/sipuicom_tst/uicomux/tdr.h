//***********************************************************************************
//行情系统 linux/windows X86/X64 通用版接口定议 v2.0
//创建日期:2013.07.29
//说明：该接口提供三种获取行情数据的方式
//1)订阅-推送方式,通过回调函数获取Level2行情，适用于每一笔tick数据均要处理的情形。
//2)订阅-设置本地行情快照存储。通过TDR_GetXXX接口从本地内存获取最新行情。
//3)请求-应答。通过TDR_ReqXXX接口，向服务器请求行情数据。
//***********************************************************************************


//***********************************************************************************
//行情接口使用步骤    v2.3
//1)TDR_Create...
//2)TDR_ConnectByDynamic/TDR_ConnectByStatic
//3)TDR_SubscribeXXX 订阅行情
//4)通过回调函数或TDR_GetXXX接口获取行情
//5)TDR_UnSubscribeXXX 取消订阅
//6)TDR_DisConnect 断开连接
//7)TDR_Destroy   销毁句柄
//***********************************************************************************



//  tdr.h   LINUX/windows   X86/X64 通用版接口定义

//  由于使用了动态库，在编译连接时要加-ldl选项.
//  如果在code::block 集成环境,Project->Build Options->Linker Setting->Other Linker Options加-ldl选项
//
//  如果您使用了多线程，需要为GCC加上pthread链接库，
//  如果在code::block集成环境，则Project->Build Options->Linker Setting->Link Libraries中加入pthread

// LINUX中 GCC类型长度(字节)
// type         x86_sizeof(type)    x64_sizeof(type)
// char         1                   1
// short        2                   2
// int          4                   4
// long         4                   8
// void*        4                   8
// long long    8                   8
// float        4                   4
// double       8                   8

//__GNUC__
//linux
//__i386__  是x86
//__x86_64__  是X64


//windows VC编译器
// type         x86_sizeof(type)    x64_sizeof(type)
// char         1                   1
// short        2                   2
// int          4                   4
// long         4                   4
// void*        4                   8
// long long    8                   8
// float        4                   4
// double       8                   8

//_WIN32
//  Defined for applications for Win32 and Win64. Always defined.
//_WIN64
//  Defined for applications for Win64.
//_WINDOWS_ 在Windows.h中定义的#ifndef _WINDOWS_
//#define _WINDOWS_

#include "tdef.h"

#ifndef TDR_H_INCLUDED
#define TDR_H_INCLUDED




//--------------------------------------------------------------------------------------------
//参数命名规范
//1 单个字符 char 以小写字母‘c’打头，若不作说明，均指小写字母。
//2 char* char[] 类型，以小写字母's'打头。
//3 有符号整型T_I32 即 n打头。
//4 无符号整型T_U32 即 u打头。
//5 long long类型以T_I64 i 打头


//-----------------------------------------------------------------------------------------
// 错误码
#define SE_OK                 0x00  // 成功
#define SE_ERR                0x01  // 未知错误
#define SE_ERRHANDLE          0x02  // 无效句柄
#define SE_ARGS               0x03  // 参数错误
#define SE_ERRDATA            0x04  // 错误的数据或数据无效
#define SE_EXP                0x05  // 错误的表达式
#define SE_FRMERR             0x07  // 报文错误
#define SE_UNINITIONAL        0x08  // 未初始化

#define SE_NOTSUPPORT         0x0F  // 不支持的命令

#define SE_NOCONNECT          0x10  // 网络未连接
#define SE_TIMEOUT            0x11  // 网络超时
#define SE_CONNECTFULL        0x12  // 服务器连接满
#define SE_NETERR             0x13  // 网络错误

#define SE_OP_NOUSER          0x20  // 无此用户
#define SE_OP_NOPOWER         0x21  // 无此权限
#define SE_OP_NOACTIVE        0x22  // 帐号不活动
#define SE_OP_PASSWORD        0x23  // 密码错误

#define SE_NOKEY              0x30  // 主键不存在
#define SE_KEYEXIST           0x31  // 主键已经存在
#define SE_NOTDEFITEM         0x32  // 没有定义的抽象数据类型

#define SE_SUBSCRIPT_FULL     0x40  // 订阅满
#define SE_NOTSUBSCRIPT       0x41  // 没有订阅
#define SE_INFOSVRNOTRUN      0x42  // info_svr没有运行或者连接失败!
#define SE_USERMAXCONNECTED   0x43  // 用户已达到最大同时登录数，不能再连接
#define SE_IPMASK             0x44  // IP被屏蔽
#define SE_VER                0x45  // 版本错误
#define SE_NOTUPLINK          0x46  // 不容许级联
#define SE_PGMCONNECTERR      0x47  // 加入可靠多播错误
#define SE_READBUFOVERFLOW    0x48  // 接收缓冲溢出
#define SE_NOPGMRECVPOWER     0x49  // 无PGM读取权限


#define SE_LIBUI              0x51  // UI库错误
#define SE_LIBMI              0x52  // MI库错误
#define SE_NOSERVER           0x53  // 没有服务器，动态连接时，当没有sip_svr运行时会返回这个错误代码.
#define SE_NOMARKET           0x54  // 无此市场
#define SE_NOCODE             0x55  // 无此编码，当不能转换为抽象ID时，返回此错误
#define SE_USERNAMENOTDIGIT   0x56  // 用户名非数字格式
#define SE_OUTSIDEUSERS       0x57  // 超出最大用户数,TDR_SubscribeTrand可能会返回这个错误
#define SE_NOSNAPSHOT         0x58  // 没有快照，是指创建时不使用快照，Get接口会返回这个错误码
#define SE_LIBERR             0x59  // 库错误，一般是没有找到库或者使用了错误的库

//证券类别定义
#define ID_BASECLASS_INDEX	  0x0000 //指数	
#define ID_BASECLASS_SHARES	  0x0100 //股票	
#define ID_BASECLASS_FUND	    0x0200 //基金	
#define ID_BASECLASS_BOND	    0x0300 //债券&可转债	
#define ID_BASECLASS_REPO	    0x0400 //回购	
#define ID_BASECLASS_QZ       0x0500 //权证	
#define ID_BASECLASS_FUTURES  0x0600 //期货	
#define ID_BASECLASS_OPTION	  0x0700 //期权	
#define ID_BASECLASS_OTHER	  0xFF00 //其他	
#define ID_BT_INDEX	          0x0001 //交易所指数	
#define ID_BT_SHARES_A	      0x0101 //A股	
#define ID_BT_SHARES_S	      0x0102 //中小板股	
#define ID_BT_SHARES_G	      0x0103 //创业板股	
#define ID_BT_SHARES_B	      0x0104 //B股	
#define ID_BT_SHARES_H	      0x0105 //H股	
#define ID_BT_SHARES_OPS	    0x0106 //优先股	
#define ID_BT_SHARES_NEEQ	    0x0108 //新三板	
#define ID_BT_SHARES_OTHER	  0x01FF //其它股票	
#define ID_BT_FUND_OPEN	      0x0201 //未上市开放基金	
#define ID_BT_FUND_LOF	      0x0202 //上市开放基金	
#define ID_BT_FUND_ETF	      0x0203 //交易型开放式指数基金	
#define ID_BT_FUND_CEF	      0x0204 //封闭式基金	
#define ID_BT_FUND_OTHER	    0x02FF //其它基金	
#define ID_BT_BOND_NA	        0x0301 //政府债券	
#define ID_BT_BOND_CORP	      0x0302 //企业债券	
#define ID_BT_BOND_FIN	      0x0303 //金融债券	
#define ID_BT_BOND_CON	      0x0304 //可转债券	
#define ID_BT_BOND_WI	        0x0305 //债券预发行	
#define ID_BT_BOND_OTHER	    0x03FF //其它债券	
#define ID_BT_REPO_NA	        0x0401 //国债回购	
#define ID_BT_REPO_CORP	      0x0402 //企债回购	
#define ID_BT_REPO_ORP	      0x0403 //买断式债券回购	
#define ID_BT_REPO_QRP	      0x0404 //报价回购	
#define ID_BT_REPO_DW	        0x0405 //质押回购	
#define ID_BT_REPO_OTHER	    0x04FF //其它回购	
#define ID_BT_QZ_CIW	        0x0501 //企业发行权证	
#define ID_BT_QZ_COV	        0x0502 //备兑权证	
#define ID_BT_QZ_OTHER	      0x05FF //其它权证	
#define ID_BT_FUTURES_IDX	    0x0601 //指数期货	
#define ID_BT_FUTURES	        0x0602 //商品期货	
#define ID_BT_FUTURES_SHA	    0x0603 //股票期货	
#define ID_BT_FUTURES_FBD	    0x0604 //债券期货	
#define ID_BT_FUTURES_OTHER	  0x06FF //其它期货	
#define ID_BT_OPTION_STOCK	  0x0701 //个股期权	
#define ID_BT_OPTION_ETF	    0x0702 //ETF期权	
#define ID_BT_OPTION_OTHER	  0x07FF //其它期权

//-----------------------------------------------------------------------------------------
// 基本数据结构
#ifndef _TPOSMAP
#define _TPOSMAP
struct tPOSMAP { // 位置结构，用于遍历代码表
  T_U32 npos;  //hash位置
  T_U32 nlist; //List位置
};
#endif

//-----------------------------------------------------------------------------------------
// 回调函数定义

// 数据到达回调，pParam为调用着自己的参数，即TDR_Create中的pParamData参数
typedef  void (__stdcall *ONRECEIVEDATA)(void* pUserParam, T_I32 nDate, 
  T_I32 nMarketId, const char* sCode, const char* sName, T_U32 uType, 
  T_I32 nServiceId, void* pData, T_I32 nLen);

// 错误信息回调，pParam为调用着自己的参数，即TDR_Create中的pParamMsg参数
typedef void (__stdcall *ONERRORMSG)(void* pUserParam,T_I32 nError,
  T_I32 nErrSource, T_U32 uData);



//-----------------------------------------------------------------------------------------
// 证券业务数据结构


// 外网运营商
#define WAN_TC                0           // 电信
#define WAN_NC                1           // 网通
#define WAN_UC                2           // 联通
#define WAN_MC                3           // 移动
#define WAN_CC                4           // 广电

// 订阅方式
#define RSS_MODE_NEW          0           // 最新订阅
#define RSS_MODE_INC          1           // 增量订阅

// 订阅推送位置
#define UI_RSS_POSSTART       0           // 订阅推送位置从最开始
#define UI_RSS_POSCUR         0XFFFFFFFF  // 订阅推送位置从当前

// 错误源定义,cb_ErrMsg回调中使用
#define ERRMSGSRC_CONNECT     0x81        // 连接
#define ERRMSGSRC_LOGIN       0x82        // 登录
#define ERRMSGSRC_MARKETSTATE 0x83        // 市场状态
#define ERRMSGSRC_REPLAY      0x84        // 实时回放

// 市场状态定义
#define MARKET_STATE_BREAK    1           // 休市
#define MARKET_STATE_CLOSE    2           // 闭市


// 登录方式
// 登录方式
#define UI_LOGIN_NORMAL       0           // 普通模式
#define UI_LOGIN_UPLINK       1           // 级联模式
#define UI_LOGIN_PGM          2           // PGM模式

// 网络模式
#define SIP_SVR_WAN           0           // SIP_SVR的外网IP
#define SIP_SVR_LAN           1           // SIP_SVR的内网IP

//代理类型
#define TCP_PROXY_NONE        0           // 不使用代理SOCKET5
#define TCP_PROXY_SOCKET5     1           // SOCKET5代理
#define TCP_PROXY_HTTP        2           // 暂不支持

//////////////////////////////////////////////////////////////////////////
//现有市场编号定义到8，若扩展期它市场，在此添加备注信息，各市场定义的宏参
//见各市场定义定义头文件
//////////////////////////////////////////////////////////////////////////
//// 市场编号定义                                                          */
//#define     SH            1       //上海市场
//#define     SZ            2       //深圳市场
//#define     CFFEX         3       //中金所
//#define     CZCE          4       //郑商所
//#define     DCE           5       //大商所
//#define     SHFE          6       //上期所
//#define     ZZZS          7       //中证指数市场
//#define     SHOP          8       //上交所期权市场
//#define     HK            9       //香港市场
//#define     SZOP          11      //深交所期权

#pragma pack(push,1)                      // 结构1字节对起，直到后面的pack(pop)，仅对业务数据结构要求。

//   1.1 市场信息
typedef struct {
  unsigned char uNumber;          // 市场编号，对应抽象ID的Byte3 ，作为唯一key
  unsigned char ucRes1;           // 保留1
  unsigned char ucRes2[2];        // 保留2
  char          sName[20];        // 市场名称
  char          sCode[8];         // 市场代码SZ,SH,CF
} Security_MarketInfo; //sizeof() = 32

//   1.2 证券代码
typedef struct {
  T_U32         uKey;             // 主键key,Byte0-Byte1:与抽象ID的Byte1-Byte2对应，取值[1-65534]；Byte2:市场编号,与T_MARKETINFO中的uNumber相对应,Byte3:0x00
  T_U32         uType;            // 证券类型
  char          sCode[28];        // 普通证券代码6位，但考虑到期权代码扩至28位
  char          sName[28];        // 证券名称
} Security_Code; //sizeof()= 64

#pragma pack(pop)  // 1字节对其结束

//当日历史数据
typedef struct t_HistoryData {
  T_U16         usLen;            // sData中有效数据的长度
  T_U32         uPos;             // 当日历史数据在内存中的存储位置
  char          sData[8186];      // 抽象数据类型，根据请求的类型定
} T_HistoryData;

//定义数据类型
typedef struct t_DataType {
  int           nMarketId;        // 市场编码
  int           nServiceId;       // 服务编码
} T_DataType;

//-------------------------------------------------------------------------------------------
//-------------------------接口调用----------------------------------------------------------
#define TDRAPI(type) type __stdcall
extern "C" {

// 创建,返回句柄
TDRAPI(T_HANDLE) TDR_Create(
  const char*     slibpath,           // [in] 库目录，不含库文件名，如果放在path中，可为NULL
  ONRECEIVEDATA   funData,            // [in] 数据到达回调函数
  void*           pParamData,         // [in] 数据到达回调函数的调用者参数
  ONERRORMSG      funError,           // [in] 错误消息回调函数
  void*           pParamMsg,          // [in] 错误消息回调函数的调用者参数。
  bool            bSnapshot,          // [in] 是否使用快照,true/false
  bool            bAutoReRss          // [in] 是否使用自动重订阅true/false
  );

// 销毁句柄
TDRAPI(T_I32) TDR_Destroy(T_HANDLE h);

//以静态方式与订阅端建立连接，可连接指定的行情服务器
TDRAPI(T_I32) TDR_ConnectByStatic(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sSvrIP,             //[in] ip地址
  T_I32           nSvrPort,           //[in] 端口号
  const char*     sUserName,          //[in] 用户名
  const char*     sPassword,          //[in] 密码
  const char*     sInfosvrIP,         //[in] Info_SVR IP地址,Info_SVR上存储市场信息、证券代码信息、用户信息等
  T_I32           nInfoSvrPort,       //[in] Info_SVR Port地址
  T_I32           nLoginMode,         //[in] 普通登录、级联登录
  int             nTimeOutSec         //[in] 登陆超时(秒)
  );

// 以动态方式与服务端建立连接,会选择一台负载最小的服务器与之连接
TDRAPI(T_I32) TDR_ConnectByDynamic(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sIP,                //[in] IP地址
  T_I32           nPort,              //[in] 端口号
  T_I32           nIPType,            //[in] 内网或外网标识 SIP_SVR_LAN:内网，SIP_SVR_WAN:外网
  T_I32           nWanType,           //[in] 网络类型,移动、电信、网通
  const char*     sUserName,          //[in] 用户名
  const char*     sPassword,          //[in] 密码
  T_I32           nLoginMode,         //[in] 普通登录、级联登录
  int             nTimeOutSec         //[in] 登陆超时(秒)
  );

// 连接回放服务器，实时回放当天的行情数据。
// 支持以两种方式控制回放的速率：
// 1. 实时行情速率的倍数(nReplaySpeed,最大8倍).采用这种方式回放时,回放服务器每一秒钟需要发送的
// 数据量为原始行情数据在内存中nReplaySpeed秒之内缓存的数据量.
// 2. 最大回放读取数据的速率(nReplayMaxRate)。采用这种方式回放时,回放服务器每一秒钟从内存中读取
// nReplayMaxRate千字节的数据. 注意,这里的读取的数据量为原始行情的数据量,服务端开启压缩的情况下实际
// 发送的数据量为压缩后的数据量,可能仅为该值的几分之一.
// 当两种方式都指定时采用第二种方式。当行情数据回放结束后进入实时数据发布模式。
// 当nReplayBeginTime=0时从内存中缓存的最早的数据开始回放，nReplayBeginTime<0时直接进入实时数据发布模式。
TDRAPI(T_I32) TDR_ConnectForReplay(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sReplaySvrIP,       //[in] 回放服务器ip地址
  T_I32           nReplaySvrPort,     //[in] 回放服务器端口号
  const char*     sUserName,          //[in] 用户名
  const char*     sPassword,          //[in] 密码
  const char*     sInfosvrIP,         //[in] Info_SVR IP地址,Info_SVR上存储市场信息、证券代码信息、用户信息等
  T_I32           nInfoSvrPort,       //[in] Info_SVR Port地址
  int             nTimeOutSec,        //[in] 登陆超时(秒)
  int             nReplayBeginTime,   //[in] 回放数据开始时间(hhmmss)
  int             nReplaySpeed,       //[in] 实时行情速率的倍数，最大8倍
  int             nReplayMaxReadRate, //[in] 最大回放读取速率(kB/s)
  T_DataType*     pReplayDataTypes,   //[in] 需要回放的数据类型数组,为空时回放全市场
  int             nDataTypeCount      //[in] 需回放的数据类型数组长度
  );

// 当前是否已连接到服务器,返回true 已连接，false没有连接或者已经断开连接
TDRAPI(bool) TDR_IsConnected(
  T_HANDLE        h                   //[in] TDR_Create返回的句柄
  );

// 断开和服务器之间的连接
TDRAPI(T_I32) TDR_DisConnect(
  T_HANDLE        h                   //[in] TDR_Create返回的句柄
  );

// 订阅指定市场中一只证券的一种数据类型.
TDRAPI(T_I32) TDR_SubscribeByCode(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  const char*     sCode,              //[in] 证券代码
  unsigned char   ucMode,             //[in] 订阅模式
  T_I32           nServiceId          //[in] 服务编码
  );

// 取消指定市场中一只证券的一种数据类型的订阅.
TDRAPI(T_I32) TDR_UnsubscribeByCode(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  const char*     sCode,              //[in] 证券代码
  T_I32           nServiceId          //[in] 服务编码
  );

// 订阅指定市场中所有证券的一种数据类型.
TDRAPI(T_I32) TDR_SubscribeByMarket(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  unsigned char   ucMode,             //[in] 订阅模式
  T_I32           nServiceId          //[in] 服务编码
  );

// 取消指定市场中所有证券的一种数据类型的订阅.
TDRAPI(T_I32) TDR_UnsubscribeByMarket(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码      
  T_I32           nServiceId          //[in] 服务编码
  );

// 订阅指定市场中一组证券的一种数据类型.
TDRAPI(T_I32) TDR_SubscribeByGroup(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //市场代码,SH、SZ、SHFE、
  const char*     sCodes,             //订阅的证券代码，多支证券以逗号分隔","，比如600000,000001,000012
  unsigned char   ucMode,             //[in] 订阅模式
  T_I32           nServiceId          //[in] 服务编码
  );

// 取消指定市场中一组证券的一种数据类型的订阅.
TDRAPI(T_I32) TDR_UnsubscribeByGroup(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarkets,           //[in] 市场代码
  const char*     sCodes,             //订阅的证券代码，多支证券以逗号分隔","，比如600000,000001,000012
  T_I32           nServiceId          //[in] 服务编码
  );

// 取消整个市场中所有证券的所有数据类型的订阅.
TDRAPI(T_I32) TDR_UnsubscribeAll(
  T_HANDLE        h                   //[in] TDR_Create返回的句柄
  );

// 获取内存中缓冲的指定市场中一只证券的一种数据类型
TDRAPI(T_I32) TDR_GetMarketData(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  const char*     sCode,              //[in] 证券代码
  T_I32           nServiceId,         //[in] 服务ID号
  void*           pData,              //[in] 输出快照数据地址
  int             nDataSize           //[in] 快照数据结构体长度
  );

// 向服务器请求指定市场中一只证券的一种数据类型
TDRAPI(T_I32) TDR_ReqMarketData(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  const char*     sCode,              //[in] 证券代码
  T_I32           nServiceId,         //[in] 服务ID号
  void*           pData,              //[in] 输出快照数据地址
  int             nDataSize           //[in] 快照数据结构体长度
  );

// 向服务器请求指定市场中一组证券的一种数据类型
TDRAPI(T_I32) TDR_ReqGroupMarketData(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  const char*     sCode,              //[in] 订阅的证券代码，多支证券以逗号分隔","，比如600000,000001,000012
  T_I32           nServiceId,         //[in] 服务ID号
  void*           pDataArray,         //[in] 输出快照数据数组地址
  int             nDataSize,          //[in] 快照数据结构体长度
  int             nCount              //[in] 快照数量(必须和sCode中证券代码的数量匹配)
  );

// 获取指定市场代码表中给定位置的第一只证券代码.
TDRAPI(bool) TDR_GetCodeTableFirst(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  tPOSMAP*        pos,                //[in] 代码表中位置
  Security_Code*  pcode               //[out] 输出的证券代码信息
  );

// 获取指定市场代码表中给定位置的下一只证券代码.
TDRAPI(bool) TDR_GetCodeTableNext(
  T_HANDLE        h,                  //[in] TDR_Create返回的句柄
  const char*     sMarket,            //[in] 市场代码
  tPOSMAP*        pPos,               //[in] 代码表中位置
  Security_Code*  pcode               //[out] 输出的证券代码信息
  );

// 获取指定市场的服务器日期.
TDRAPI(T_I32) TDR_GetMarketDate(
  T_HANDLE        h,                  // [in] TDR_Create返回的句柄
  T_I32           nMarket,            // [in] 市场编码
  T_I32*          nDate               // [out] 返回SE_O时回填交易日期
  );

// 请求指定市场中一只证券在内存中缓存的历史数据
TDRAPI(T_I32) TDR_ReqHistoryData(
  T_HANDLE        h,                  // [in] TDR_Create返回的句柄
  const char*     sMarket,            // [in] 市场代码
  const char*     sCode,              // [in] 证券代码或合约代码
  T_I32           nServiceId,         // [in] 服务数据类型
  T_U32           uPos,               // [in] 请求数据位置，填0表示从头开始请求
  T_HistoryData   pHisData[],         // [in/out] 返回数据存储空间
  T_I32           nSize,              // [in] T_HistoryData数据组大小
  T_I32*          pnRecs              // [out] 返回的实际数据大小2
  );

// 设置代理服务器
TDRAPI(T_I32) TDR_SetProxyServer(
  T_HANDLE        h,                  // [in] UI_Create创建的句柄
  T_U16           sutype,             // [in] 代理类型
  const char*     sip,                // [in] 代理服务器IP
  T_U16           suport,             // [in] 代理服务器端口
  const char*     suser,              // [in] 连接代理服务器的用户名
  const char*     spass               // [in] 连接代理服务器的密码
  );

}

#endif // TDR_H_INCLUDED
