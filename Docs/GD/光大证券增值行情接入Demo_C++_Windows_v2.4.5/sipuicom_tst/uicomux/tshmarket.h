#ifndef _T_SH_MARKET_
#define _T_SH_MARKET_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

// �г���Ŷ���                                                          */
#define     SH                1     //�Ϻ��г�

//*****************************************************************************************
//���Ϸ�������ID������ԭϵͳ���ݣ����·���ID���ÿ���г��ֿ�����
//-----------------------------------�Ϻ��г�--------------------------------------
#define ID_SH_INDEXDATA       0x00  //ָ��(Stock_IndexData)
#define ID_SH_TRANSACTION     0x01  //�ɽ�(Stock_Transaction)
#define ID_SH_ORDERQUEUE      0x02  //ί�ж���(Stock_OrderQueue_Head+Stock_OrderQueue)
#define ID_SH_MARKETDATA      0x04  //��������(Stock_MarketData)
#define ID_SH_MARKETDATA_L1   0x05  //����L1���� �Ϻ�(Stock_MarketData_L1)
#define ID_SH_KLINEDATA       0x07  //�Ͻ������ɷ���K������(T_SH_Kline)

#pragma pack(push,1)

// 1.1 ��Ʊ����
typedef struct t_SH_StockMarketDataL2 {
  T_I32 nTime;                      //ʱ��(HHMMSSmmmm)
  T_I32 nStatus;                    //״̬
  T_U32 uPreClose;                  //ǰ���̼�
  T_U32 uOpen;                      //���̼�
  T_U32 uHigh;                      //��߼�
  T_U32 uLow;                       //��ͼ�
  T_U32 uMatch;                     //���¼�
  T_U32 uAskPrice[10];              //������
  T_U32 uAskVol[10];                //������
  T_U32 uBidPrice[10];              //�����
  T_U32 uBidVol[10];                //������
  T_U32 uNumTrades;                 //�ɽ�����
  T_I64 iVolume;                    //�ɽ�����
  T_I64 iTurnover;                  //�ɽ��ܽ��
  T_I64 iTotalBidVol;               //ί����������
  T_I64 iTotalAskVol;               //ί����������
  T_U32 uWeightedAvgBidPrice;       //��Ȩƽ��ί��۸�
  T_U32 uWeightedAvgAskPrice;       //��Ȩƽ��ί���۸�
  T_I32 nIOPV;                      //IOPV��ֵ��ֵ
  T_I32 nYieldToMaturity;           //����������
  T_U32 uHighLimited;               //��ͣ��
  T_U32 uLowLimited;                //��ͣ��
  char sPrefix[4];                  //֤ȯ��Ϣǰ׺
  T_I32 nSyl1;                      //��ӯ��1 2 λС�� ��Ʊ���۸�/����ÿ������ ծȯ��ÿ��ԪӦ����Ϣ
  T_I32 nSyl2;                      //��ӯ��2 2 λС�� ��Ʊ���۸�/����ÿ������ ծȯ������������ ����ÿ�ٷݵ�IOPV ��ֵ Ȩ֤�������
  T_I32 nSD2;                       //����2���Ա���һ�ʣ�
  char sTradingPhraseCode[8];       //���ֶ�Ϊ8λ�ַ���������ÿλ��ʾ�ض��ĺ��壬�޶�������ո񡣵�1λ����S����ʾ����������ǰ��ʱ�Σ���C����ʾ���Ͼ���ʱ�Σ���T����ʾ��������ʱ�Σ���B����ʾ����ʱ�Σ���E����ʾ����ʱ�Σ���P����ʾ��Ʒͣ�ơ�
  T_I32 nPreIOPV;                   //���� T-1 ������ʱ�� IOPV �����Ϊ����ʱ��Ч
} Stock_MarketData,T_SH_StockMarketDataL2,*PSH_StockMarketDataL2;

//1.2 dbf���飬�Ͻ�����������ô˽ṹ
typedef struct t_SH_StockMarketDataL1 {
  T_I32 nTime;                      //ʱ��(HHMMSSmmmm)
  T_I32 nStatus;                    //״̬
  T_U32 uPreClose;                  //ǰ���̼�
  T_U32 uOpen;                      //���̼�
  T_U32 uHigh;                      //��߼�
  T_U32 uLow;                       //��ͼ�
  T_U32 uMatch;                     //���¼�
  T_U32 uAskPrice[5];               //������
  T_U32 uAskVol[5];                 //������
  T_U32 uBidPrice[5];               //�����
  T_U32 uBidVol[5];                 //������
  T_U32 uNumTrades;                 //�ɽ�����
  T_I64 iVolume;                    //�ɽ�����
  T_I64 iTurnover;                  //�ɽ��ܽ��
  T_U32 uHighLimited;               //��ͣ��
  T_U32 uLowLimited;                //��ͣ��
  char sTradingPhaseCode[8];        //���ֶ�Ϊ8λ�ַ���������ÿλ��ʾ�ض��ĺ��壬�޶�������ո񡣵�1λ����S����ʾ����������ǰ��ʱ�Σ���C����ʾ���Ͼ���ʱ�Σ���T����ʾ��������ʱ�Σ���B����ʾ����ʱ�Σ���E����ʾ����ʱ�Σ���P����ʾ��Ʒͣ�ơ�
  T_I32 nPreIOPV;                   //����T-1������ʱ��IOPV  MDStreamID == MD004 ��ʾ����ʱ��Ч
  T_I32 nIOPV;                      //����IOPV  MDStreamID == MD004 ��ʾ����ʱ��Ч

  //2018-03-30	���ӡ��������̼ۡ��ֶΣ�����3�������ֶ�
  T_U32 uClosePrice;                //�������̼�
  T_U32 uResv1;						//�����ֶ�1
  T_U32 uResv2;						//�����ֶ�2
  T_U32 uResv3;						//�����ֶ�3
} Stock_MarketData_L1,T_SH_StockMarketDataL1,*PSH_StockMarketDataL1;


//1.3 ��ʳɽ�(Transaction)
typedef struct t_SH_StockStepTrade {
  T_I32 nTradeIndex;                //�ɽ����
  T_I32 nTradeChannel;              //�ɽ�ͨ��
  T_I32 nTradeTime;                 //�ɽ�ʱ�� HHMMSSmmm
  T_I32 nTradePrice;                //�ɽ��۸� ����10000��
  T_I64 iTradeQty;                  //�ɽ����� ��Ʊ���� Ȩ֤���� ծȯ����
  T_I64 iTradeMoney;                //�ɽ����(Ԫ)
  T_I64 iTradeBuyNo;                //�򷽶�����
  T_I64 iTradeSellNo;               //����������
  char cTradeBSflag;                //�����̱�ʶ B -���̣�������  S-����,������ N δ֪
  char sRes[3];                     //�����ֶ�1
} Stock_Transaction_SH,T_SH_StockStepTrade,*PSH_StockStepTrade; //�Ͻ�����ʳɽ�����Ӧ������UA3201



//1.4 ��������(Queue)
#ifndef _ORDER_QUEUE_
#define _ORDER_QUEUE_
typedef struct t_OrderQueueHead {
  T_I32 nItem;                      //���ݸ���
} Stock_OrderQueue_Head,T_OrderQueueHead,*POrderQueueHead;
typedef struct t_OrderQueueItem {
  T_I32 nTime;                      //����ʱ��(HHMMSSmmmm)
  T_I32 nSide;                      //��������('B':Bid 'S':Ask)
  T_I32 nPrice;                     //�ɽ��۸�
  T_I32 nOrders;                    //��������
  T_I32 nABItems;                   //��ϸ����
  T_I32 nABVolume[200];             //������ϸ
} Stock_OrderQueue,T_OrderQueueItem,*POrderQueueItem;
#endif //_ORDER_QUEUE_

typedef struct t_SH_StockOrderQueue {
  T_OrderQueueHead tHead;
  T_OrderQueueItem tItem[0];
} T_SH_StockOrderQueue,*PSH_StockOrderQueue;

//1.5 ָ��
typedef struct t_SH_StockIndex {
  T_I32 nTime;                      //ʱ��(HHMMSSmmmm)
  T_I32 nOpenIndex;                 //����ָ��
  T_I32 nHighIndex;                 //���ָ��
  T_I32 nLowIndex;                  //���ָ��
  T_I32 nLastIndex;                 //����ָ��
  T_I64 iTotalVolume;               //���������Ӧָ���Ľ�������
  T_I64 iTurnover;                  //���������Ӧָ���ĳɽ����
  T_I32 nPreCloseIndex;             //ǰ����ָ��
  T_I32 nCloseIndex;				//������ָ��
} Stock_IndexData,T_SH_StockIndex,*PSH_StockIndex;

//1.6 ����K��
typedef struct t_SH_Kline {
  T_U32 uDay;                       // ����        YYYYMMDD
  T_I32 nTime;                      // ʱ��(����ʱ��)  HHMM
  T_I32 nPreClose;                  // ǰ���̼�         ��λ��1/100��
  T_I32 nValOpen;                   // ���̼�      ��λ��1/100��,����1��ʾ0.0001Ԫ
  T_I32 nValHigh;                   // ��߼�      ��λ��1/100��
  T_I32 nValLow;                    // ��ͼ�      ��λ��1/100��
  T_I32 nValClose;                  // ���̼�      ��λ��1/100��
  T_I64 i64Volume;                  // �����ڳɽ���    ��λ����֤ȯ����С���׵�λ�������ƱΪ���ɡ�
  T_I64 i64ValTotal;                // �����ڳɽ���    ��λ��Ԫ
  T_I64 i64TotalVol;                // �ۼƳɽ���    ��λ����֤ȯ����С���׵�λ�������ƱΪ���ɡ�
  T_I64 i64TotalTurnOver;           // �ۼƳɽ����    ��λ��Ԫ
  T_I32 nTurover;                   // ����(�ٷ���)    ��λ��1/10000������1��ʾ0.01%
  T_I32 nValIncrease;               // �ǵ�ֵ      ��λ��1/100��
} T_SH_Kline,*PSH_Kline; // sizeof() = 48
#pragma pack(pop)
#endif //_T_SH_MARKET_