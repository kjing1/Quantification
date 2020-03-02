#ifndef _T_SHHKMARKET_H_ 
#define _T_SHHKMARKET_H_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

#define SHHK                  13             //香港市场

#define ID_SHHK_INDEX         0x00  //指数(Stock_Index)
#define ID_SHHK_SNAPSHOT      0x01  //快照(Stock_Snapshot)
#define ID_SHHK_TRADETICK     0x02  //分笔成交(Stock_TradeTick)
#define ID_SHHK_ODDLOT        0x03  //碎股订单(Stock_OddLot)

#pragma pack(push,1)

//指数 ua2213 
typedef struct t_SHHK_StockIndex {
  T_I32 nIndexTime;                         //指数时间
  T_I32 nDataTimeStamp;                     //时间戳,行情发送时间
  char IndexSource;                         //指数来源
  char sCurrencyCode[4];                    //汇率代码
  char IndexStatus;                         //指数状态
  T_I64 nIndexValue;                        //指数
  T_I64 nNetChgPreDay;                      //指数变化
  T_I64 nHighValue;                         //最高指数
  T_I64 nLowValue;                          //最低指数
  T_I64 nEASValue;                          //均值
  T_I64 nIndexTurnover;                     //成交额
  T_I64 nOpeningValue;                      //开盘指数
  T_I64 nClosingValue;                      //收盘指数
  T_I64 nPreviousSesClose;                  //前收盘指数
  T_I64 nIndexVolume;                       //成交量
  T_I32 nNetChgPreDayPct;                   //指数变化率
} T_SHHK_StockIndex,*PSHHK_StockIndex;              

//快照 ua2202 ua2206 ua2207
typedef struct t_SHHK_StockSnapshot {
  T_I32 nTime;                             //时间
  T_I32 nHighPx;                           //最高价
  T_I32 nLowPx;                            //最低价
  T_I32 nLastPx;                           //现价
  T_I32 nClosePx;                          //收盘价
  T_I32 nNorminalPx;                       //按盘价
  T_I64 nBidSize[10];                      //申买量
  T_I32 nBidPx[10];                        //申买价
  T_I64 nOfferSize[10];                    //申卖量
  T_I32 nOfferPx[10];                      //申卖价
  T_I32 nYield;                            //债券收益
  T_I32 nShortSellSharesTraded;            //抛空数量
  T_I64 nShortSellTurnover;                //抛空金额
  T_I64 nTotalVolumeTrade;                 //成交数量
  T_I64 nTotalValueTrade;                  //成交金额
  T_I32 nTradingStatus;                    //交易状态
  T_I32 nCASReffPrice;                     //CAS 的参考价格
  T_I32 nCASLowerPrice;                    //CAS 下限价
  T_I32 nCASUpperPrice;                    //CAS 上限价
  char OrdImbDirection;                    //CAS 未能配对买卖盘的方向
  T_I64 nOrdImbQty;                        //CAS 未能配对买卖盘的数量
} T_SHHK_StockSnapshot,*PSHHK_StockSnapshot;  

//分笔成交 ua2203 
typedef struct t_SHHK_StockTradeTick {
  T_I32 nTradeTime;                          //时间
  T_I32 nTickId;                             //成交序号
  T_I32 nPrice;                              //成交价格
  T_I64 nAggregateQuantity;                  //成交量
  T_I32 nTradeType;                          //成交类型
  char TradeCancelFlag;                      //是否取消
} T_SHHK_StockTradeTick,*PSHHK_StockTradeTick;  

//碎骨订单 ua2204 
typedef struct t_SHHK_StockOddLot {
  T_I32 nDataTimeStamp;                      //时间戳,行情发送时间
  T_I64 nOrderID[10];                        //订单编号
  T_I32 nPrice[10];                          //价格
  T_I64 nOrderQty[10];                       //量
  T_I32 nBrokerID[10];                       //经纪人编号
  T_I32 nSide[10];                           //买卖方向
} T_SHHK_StockOddLot,*PSHHK_StockOddLot;  

#pragma pack(pop)
#endif //_T_HKMARKET_H_