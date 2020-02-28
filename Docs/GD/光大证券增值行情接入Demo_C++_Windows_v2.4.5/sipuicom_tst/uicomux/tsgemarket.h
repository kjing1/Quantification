#ifndef _T_SGE_MARKET_
#define _T_SGE_MARKET_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

// 市场编号定义                                                          */
#define     SGE                 12     //上海黄金市场

//*****************************************************************************************
//以上服务数据ID保留与原系统兼容，以下服务ID针对每个市场分开定义
//-----------------------------------上海黄金市场--------------------------------------
#define ID_SGE_MARKETDATA       0x01  //市场数据(t_SGE_MarketData)


#pragma pack(push,1)

// 1.1 贵金属行情
typedef struct t_SGE_MarketData {
  T_U32 uTradeDate;           /*交易日期*/
  T_I32 nTime;                /*生成时间*/
  T_U32	uTID;                 /*事务编号*/
  T_U32	uLastPrice;           /*最新价*/
  T_U32	uHighPrice;           /*最高价*/
  T_U32	uLowPrice;            /*最低价*/
  T_U32	uLastMatchQty;        /*最新成交量*/
  T_I64	iMatchTotQty;         /*成交量*/
  T_I64	iMatchWeight;         /*成交重量*/
  T_I64	iTurnover;            /*成交额*/
  T_U32	iInitOpenInterest;    /*初始持仓量*/
  T_U32	uOpenInterest;        /*持仓量*/
  T_I32	nInterestChg;         /*持仓量变化*/
  T_U32	uClearPrice;          /*今结算价*/
  T_U32	uLifeLow;             /*历史最低价*/
  T_U32	uLifeHigh;            /*历史最高价*/
  T_U32	uRiseLimit;           /*涨停板*/
  T_U32	uFallLimit;           /*跌停板*/
  T_U32	uLastClearPrice;      /*上日结算价*/
  T_U32	uLastClose;           /*上日收盘价*/
  T_U32	uHightBidPrice;       /*最高买*/
  T_U32	uBidQty;              /*申买量*/
  T_U32	uBidImplyQty;         /*申买推导量*/
  T_U32	uLowestAskPrice;      /*最低卖*/
  T_U32	uAskQty;              /*申卖量*/
  T_U32	uAskImplyQty;         /*申卖推导量*/
  T_U32	uAvgPrice;			      /*当日均价*/
  T_U32	uOpenPrice;           /*开盘价*/
  T_U32	uClosePrice;          /*收盘价*/
  T_U32	uSeqNum;              /*行情序号*/
  T_U32 uAskPrice[10];        /*申卖价*/
  T_U32 uAskVol[10];          /*申卖量*/
  T_U32 uBidPrice[10];        /*申买价*/
  T_U32 uBidVol[10];          /*申买量*/
} T_SGE_MarketData,*PSGE_MarketData;


#pragma pack(pop)
#endif //_T_SGE_MARKET_