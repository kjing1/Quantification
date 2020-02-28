#ifndef _T_SHHKMARKET_H_ 
#define _T_SHHKMARKET_H_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

#define SHHK                  13             //����г�

#define ID_SHHK_INDEX         0x00  //ָ��(Stock_Index)
#define ID_SHHK_SNAPSHOT      0x01  //����(Stock_Snapshot)
#define ID_SHHK_TRADETICK     0x02  //�ֱʳɽ�(Stock_TradeTick)
#define ID_SHHK_ODDLOT        0x03  //��ɶ���(Stock_OddLot)

#pragma pack(push,1)

//ָ�� ua2213 
typedef struct t_SHHK_StockIndex {
  T_I32 nIndexTime;                         //ָ��ʱ��
  T_I32 nDataTimeStamp;                     //ʱ���,���鷢��ʱ��
  char IndexSource;                         //ָ����Դ
  char sCurrencyCode[4];                    //���ʴ���
  char IndexStatus;                         //ָ��״̬
  T_I64 nIndexValue;                        //ָ��
  T_I64 nNetChgPreDay;                      //ָ���仯
  T_I64 nHighValue;                         //���ָ��
  T_I64 nLowValue;                          //���ָ��
  T_I64 nEASValue;                          //��ֵ
  T_I64 nIndexTurnover;                     //�ɽ���
  T_I64 nOpeningValue;                      //����ָ��
  T_I64 nClosingValue;                      //����ָ��
  T_I64 nPreviousSesClose;                  //ǰ����ָ��
  T_I64 nIndexVolume;                       //�ɽ���
  T_I32 nNetChgPreDayPct;                   //ָ���仯��
} T_SHHK_StockIndex,*PSHHK_StockIndex;              

//���� ua2202 ua2206 ua2207
typedef struct t_SHHK_StockSnapshot {
  T_I32 nTime;                             //ʱ��
  T_I32 nHighPx;                           //��߼�
  T_I32 nLowPx;                            //��ͼ�
  T_I32 nLastPx;                           //�ּ�
  T_I32 nClosePx;                          //���̼�
  T_I32 nNorminalPx;                       //���̼�
  T_I64 nBidSize[10];                      //������
  T_I32 nBidPx[10];                        //�����
  T_I64 nOfferSize[10];                    //������
  T_I32 nOfferPx[10];                      //������
  T_I32 nYield;                            //ծȯ����
  T_I32 nShortSellSharesTraded;            //�׿�����
  T_I64 nShortSellTurnover;                //�׿ս��
  T_I64 nTotalVolumeTrade;                 //�ɽ�����
  T_I64 nTotalValueTrade;                  //�ɽ����
  T_I32 nTradingStatus;                    //����״̬
  T_I32 nCASReffPrice;                     //CAS �Ĳο��۸�
  T_I32 nCASLowerPrice;                    //CAS ���޼�
  T_I32 nCASUpperPrice;                    //CAS ���޼�
  char OrdImbDirection;                    //CAS δ����������̵ķ���
  T_I64 nOrdImbQty;                        //CAS δ����������̵�����
} T_SHHK_StockSnapshot,*PSHHK_StockSnapshot;  

//�ֱʳɽ� ua2203 
typedef struct t_SHHK_StockTradeTick {
  T_I32 nTradeTime;                          //ʱ��
  T_I32 nTickId;                             //�ɽ����
  T_I32 nPrice;                              //�ɽ��۸�
  T_I64 nAggregateQuantity;                  //�ɽ���
  T_I32 nTradeType;                          //�ɽ�����
  char TradeCancelFlag;                      //�Ƿ�ȡ��
} T_SHHK_StockTradeTick,*PSHHK_StockTradeTick;  

//��Ƕ��� ua2204 
typedef struct t_SHHK_StockOddLot {
  T_I32 nDataTimeStamp;                      //ʱ���,���鷢��ʱ��
  T_I64 nOrderID[10];                        //�������
  T_I32 nPrice[10];                          //�۸�
  T_I64 nOrderQty[10];                       //��
  T_I32 nBrokerID[10];                       //�����˱��
  T_I32 nSide[10];                           //��������
} T_SHHK_StockOddLot,*PSHHK_StockOddLot;  

#pragma pack(pop)
#endif //_T_HKMARKET_H_