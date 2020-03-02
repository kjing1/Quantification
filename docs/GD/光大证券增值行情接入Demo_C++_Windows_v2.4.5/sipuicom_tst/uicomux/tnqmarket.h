
#ifndef _T_NQ_MARKET_
#define _T_NQ_MARKET_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

// �г���Ŷ���
#define NEEQ                15    //�������г�

//*****************************************************************************************
//���Ϸ�������ID������ԭϵͳ���ݣ����·���ID���ÿ���г��ֿ�����
//-----------------------------------�Ϻ��г�--------------------------------------
#define ID_NEEQ_INDEXDATA  0x00   //ָ������(Stock_IndexData)
#define ID_NEEQ_MARKETDATA 0x01   //��������(Stock_MarketData)

#pragma pack(push,1)

//1.1 ָ��
typedef struct t_NQ_StockIndex {
  T_I32 nTime;                //ʱ��(HHMMSSmmmm)
  T_I32 nOpenIndex;           //����ָ��
  T_I32 nHighIndex;           //���ָ��
  T_I32 nLowIndex;            //���ָ��
  T_I32 nLastIndex;           //����ָ��
  T_I64 iTotalVolume;         //���������Ӧָ���Ľ�������
  T_I64 iTurnover;            //���������Ӧָ���ĳɽ����
  T_I32 nPreCloseIndex;       //ǰ��ָ��
  T_I32 nContractPosition;	  //��Լ�ֲ���/(ָ��)ת������
} T_NQ_StockIndex, *PNQH_StockIndex;

// 1.2 ��Ʊ����
typedef struct t_NQ_StockMarketData {
  T_I32 nTime;                //ʱ��(HHMMSSmmmm)
  T_I32 nStatus;              //״̬
  T_U32 uPreClose;            //ǰ���̼�
  T_U32 uOpen;                //���̼�
  T_U32 uHigh;                //��߼�
  T_U32 uLow;                 //��ͼ�
  T_U32 uMatch;               //���¼�
  T_U32 uAskPrice[10];        //������
  T_U32 uAskVol[10];          //������
  T_U32 uBidPrice[10];        //�����
  T_U32 uBidVol[10];          //������
  T_U32 uMMAskPrice[10];      //������������
  T_U32 uMMAskVol[10];        //������������
  T_U32 uMMBidPrice[10];      //�����������
  T_U32 uMMBidVol[10];        //������������
  T_U32 uNumTrades;           //�ɽ�����
  T_I64 iVolume;              //�ɽ�����
  T_I64 iTurnover;            //�ɽ��ܽ��
  T_I64 iTotalBidVol;         //ί����������
  T_I64 iTotalAskVol;         //ί����������
  T_U32 uWeightedAvgBidPrice; //��Ȩƽ��ί��۸�
  T_U32 uWeightedAvgAskPrice; //��Ȩƽ��ί���۸�
  T_I32 nIOPV;                //IOPV��ֵ��ֵ
  T_I32 nYieldToMaturity;     //����������
  T_U32 uHighLimited;         //��ͣ��
  T_U32 uLowLimited;          //��ͣ��
  char  sPrefix[4];           //֤ȯ��Ϣǰ׺
  T_I32 nSyl1;                //��ӯ��1 2 λС�� ��Ʊ���۸�/����ÿ������ ծȯ��ÿ��ԪӦ����Ϣ
  T_I32 nSyl2;                //��ӯ��2 2 λС�� ��Ʊ���۸�/����ÿ������ ծȯ������������ ����ÿ�ٷݵ�IOPV ��ֵ Ȩ֤�������
  T_I32 nSD2;                 //����2���Ա���һ�ʣ�
} T_NQ_StockMarketData, *PNQ_StockMarketData;

#pragma pack(pop)

#endif //_T_NQ_MARKET_