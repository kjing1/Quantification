#ifndef _T_SGE_MARKET_
#define _T_SGE_MARKET_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

// �г���Ŷ���                                                          */
#define     SGE                 12     //�Ϻ��ƽ��г�

//*****************************************************************************************
//���Ϸ�������ID������ԭϵͳ���ݣ����·���ID���ÿ���г��ֿ�����
//-----------------------------------�Ϻ��ƽ��г�--------------------------------------
#define ID_SGE_MARKETDATA       0x01  //�г�����(t_SGE_MarketData)


#pragma pack(push,1)

// 1.1 ���������
typedef struct t_SGE_MarketData {
  T_U32 uTradeDate;           /*��������*/
  T_I32 nTime;                /*����ʱ��*/
  T_U32	uTID;                 /*������*/
  T_U32	uLastPrice;           /*���¼�*/
  T_U32	uHighPrice;           /*��߼�*/
  T_U32	uLowPrice;            /*��ͼ�*/
  T_U32	uLastMatchQty;        /*���³ɽ���*/
  T_I64	iMatchTotQty;         /*�ɽ���*/
  T_I64	iMatchWeight;         /*�ɽ�����*/
  T_I64	iTurnover;            /*�ɽ���*/
  T_U32	iInitOpenInterest;    /*��ʼ�ֲ���*/
  T_U32	uOpenInterest;        /*�ֲ���*/
  T_I32	nInterestChg;         /*�ֲ����仯*/
  T_U32	uClearPrice;          /*������*/
  T_U32	uLifeLow;             /*��ʷ��ͼ�*/
  T_U32	uLifeHigh;            /*��ʷ��߼�*/
  T_U32	uRiseLimit;           /*��ͣ��*/
  T_U32	uFallLimit;           /*��ͣ��*/
  T_U32	uLastClearPrice;      /*���ս����*/
  T_U32	uLastClose;           /*�������̼�*/
  T_U32	uHightBidPrice;       /*�����*/
  T_U32	uBidQty;              /*������*/
  T_U32	uBidImplyQty;         /*�����Ƶ���*/
  T_U32	uLowestAskPrice;      /*�����*/
  T_U32	uAskQty;              /*������*/
  T_U32	uAskImplyQty;         /*�����Ƶ���*/
  T_U32	uAvgPrice;			      /*���վ���*/
  T_U32	uOpenPrice;           /*���̼�*/
  T_U32	uClosePrice;          /*���̼�*/
  T_U32	uSeqNum;              /*�������*/
  T_U32 uAskPrice[10];        /*������*/
  T_U32 uAskVol[10];          /*������*/
  T_U32 uBidPrice[10];        /*�����*/
  T_U32 uBidVol[10];          /*������*/
} T_SGE_MarketData,*PSGE_MarketData;


#pragma pack(pop)
#endif //_T_SGE_MARKET_