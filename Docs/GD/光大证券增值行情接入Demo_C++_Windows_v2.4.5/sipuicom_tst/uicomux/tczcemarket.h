#ifndef _T_CZCE_MARKET_
#define _T_CZCE_MARKET_
#include "tdef.h"
// �г���Ŷ���                                                          */

#define     CZCE                4           //֣����






//*****************************************************************************************
//���Ϸ�������ID������ԭϵͳ���ݣ����·���ID���ÿ���г��ֿ�����


//-----------------------------------֣����-----------------------------------------------
#define ID_CZCE_MARKETDATA      0x01   //�ڻ���������(Futures_MarketData)  1016
#define ID_CZCE_BASEINFO        0x02   //�ڻ�������Ϣ
#define ID_CZCE_FORQOUTE       0x03    //ѯ��֪ͨ

#pragma pack(push,1)
//1.1 ֣�����ڻ�����
typedef struct t_CZCE_FutursMarketData {
  T_I32 nTime;                         //ʱ��(HHMMSSmmmm)
  T_I32 nStatus;                       //״̬
  T_I64 iPreOpenInterest;              //��ֲ�
  T_U32 uPreClose;                     //�����̼�
  T_U32 uPreSettlePrice;               //�����
  T_U32 uOpen;                         //���̼�
  T_U32 uHigh;                         //��߼�
  T_U32 uLow;                          //��ͼ�
  T_U32 uMatch;                        //���¼�
  T_I64 iVolume;                       //�ɽ�����
  T_I64 iTurnover;                     //�ɽ��ܽ��
  T_I64 iOpenInterest;                 //�ֲ�����
  T_U32 uClose;                        //������
  T_U32 uSettlePrice;                  //�����
  T_U32 uHighLimited;                  //��ͣ��
  T_U32 uLowLimited;                   //��ͣ��
  T_I32 nPreDelta;                     //����ʵ��
  T_I32 nCurrDelta;                    //����ʵ��
  T_U32 uAskPrice[5];                  //������
  T_U32 uAskVol[5];                    //������
  T_U32 uBidPrice[5];                  //�����
  T_U32 uBidVol[5];                    //������
} T_CZCE_FutursMarketData,*PCZCE_FutursMarketData;
//1.2 ֣�����ڻ�������Ϣ
/////��Ʒ����-------------------------------------------------------
#define THOST_FTDC_PC_Futures '1'      //�ڻ�
#define THOST_FTDC_PC_Options '2'      //�ڻ���Ȩ
#define THOST_FTDC_PC_Combination '3'  //���
#define THOST_FTDC_PC_Spot '4'         //����
#define THOST_FTDC_PC_EFP '5'          //��ת��
#define THOST_FTDC_PC_SpotOption '6'   //�ֻ���Ȩ
//��Լ��������----------------------------------------
#define THOST_FTDC_IP_NotStart '0'     //δ����
#define THOST_FTDC_IP_Started '1'      //����
#define THOST_FTDC_IP_Pause '2'        //ͣ��
#define THOST_FTDC_IP_Expired '3'      //����
//�ֲ�����-------------------------------------------------
#define THOST_FTDC_PT_Net '1'          //���ֲ�
#define THOST_FTDC_PT_Gross '2'        //�ۺϳֲ�

////////////////////////////////////////////////////////////////////////
//////�ֲ���������
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_PDT_UseHistory '1'   //ʹ����ʷ�ֲ�
#define THOST_FTDC_PDT_NoUseHistory '2' //��ʹ����ʷ�ֲ�

////////////////////////////////////////////////////////////////////////
///���߱�֤���㷨����
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_MMSA_NO '0'         //��ʹ�ô��߱�֤���㷨
#define THOST_FTDC_MMSA_YES '1'        //ʹ�ô��߱�֤���㷨

////////////////////////////////////////////////////////////////////////
///��Ȩ��������
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_CP_CallOptions '1'  //����
#define THOST_FTDC_CP_PutOptions '2'   //����

////////////////////////////////////////////////////////////////////////
///�����������
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_COMBT_Future '0'    //�ڻ����
#define THOST_FTDC_COMBT_BUL '1'       //��ֱ�۲�BUL
#define THOST_FTDC_COMBT_BER '2'       //��ֱ�۲�BER
#define THOST_FTDC_COMBT_STD '3'       //��ʽ���
#define THOST_FTDC_COMBT_STG '4'       //���ʽ���
#define THOST_FTDC_COMBT_PRT '5'       //�������
#define THOST_FTDC_COMBT_CLD '6'       //ʱ��۲����

typedef struct t_CZCE_BaseInfo {
  char sInstrumentID[31];             //��Լ����
  char sExchangeID[9];                //����������
  char sInstrumentName[21];           //��Լ���� 
  char sExchangeInstID[31];           //��Լ�ڽ������Ĵ���
  char sProductID[31];                //��Ʒ���� 
  char cProductClass;                 //��Ʒ����
  T_I32 nDeliveryYear;                //�������
  T_I32 nDeliveryMonth;               //������
  T_I32 nMaxMarketOrderVolume;        //�м۵�����µ���
  T_I32 nMinMarketOrderVolume;        //�м۵���С�µ���
  T_I32 nMaxLimitOrderVolume;         //�޼۵�����µ���
  T_I32 nMinLimitOrderVolume;         //�޼۵���С�µ���
  T_I32 nVolumeMultiple;              //��Լ��������
  T_I64 i64PriceTick;                 //��С�䶯��λ,����10000��
  T_I32 nCreateDate;                  //������
  T_I32 nOpenDate;                    //������
  T_I32 nExpireDate;                  //������
  T_I32 nStartDelivDate;              //��ʼ������
  T_I32 nEndDelivDate;                //����������
  char cInstLifePhase;                //��Լ��������״̬
  T_I32 nIsTrading;                   //��ǰ�Ƿ���
  char cPositionType;                 //�ֲ�����
  char cPositionDateType;             //�ֲ���������
  T_I64 i64LongMarginRatio;           //��ͷ��֤����,������10000��
  T_I64 i64ShortMarginRatio;          //��ͷ��֤����,������10000��
  char cMaxMarginSideAlgorithm;       //�Ƿ�ʹ�ô��߱�֤���㷨
  char sUnderlyingInstrID[31];        //������Ʒ����
  T_I64 i64StrikePrice;               //ִ�м�,������10000��
  char cOptionsType;                  //��Ȩ����
  T_I64 i64UnderlyingMultiple;        //��Լ������Ʒ����,������10000��
  char cCombinationType;              //�������
} T_CZCE_BaseInfo,*PCZCE_BaseInfo;

///���������̵�ѯ������
typedef struct t_CZCE_ForQuote {
  T_I32 nTradingDay;                   //������
  char sInstrumentID[31];              //��Լ����
  char sForQuoteSysID[21];             //ѯ�۱��
  T_I32 nForQuoteTime;                 //ѯ��ʱ��
  int nActionDay;                      //ҵ������ 
  char sExchangeID[9];                 //����������
} T_CZCE_ForQuote;
#pragma pack(pop)
#endif //_T_CZCE_MARKET_