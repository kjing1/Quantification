#ifndef _T_CFFEX_MARKET_
#define _T_CFFEX_MARKET_
#include "tdef.h"


// �г���Ŷ���                                                          */

#define     CFFEX               3           //�н���

//*****************************************************************************************
//���Ϸ�������ID������ԭϵͳ���ݣ����·���ID���ÿ���г��ֿ�����

//-----------------------------------�н���-----------------------------------------------
#define ID_CFFEX_MARKETDATA			0x01  //�ڻ�����Ȩ��������(Futures_MarketData)  1016
#define ID_CFFEX_BASEINFO			0X02  //��Ȩ����Ȩ������Ϣ
#define ID_CFFEX_FORQOUTE			0x03  //ѯ��֪ͨ
#define ID_CFFEX_INSTRUMENT_STATUS	0x04  //��Լ״̬֪ͨ
#define ID_CFFEX_DEPTH_MARKETDATA   0x05  //�ڻ�����Ȩ�����������(Futures_MarketData)  1016


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

//�ֲ�����------------------------------------------------
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
#define THOST_FTDC_MMSA_NO '0'          //��ʹ�ô��߱�֤���㷨
#define THOST_FTDC_MMSA_YES '1'         //ʹ�ô��߱�֤���㷨

////////////////////////////////////////////////////////////////////////
///��Ȩ��������
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_CP_CallOptions '1'   //����
#define THOST_FTDC_CP_PutOptions '2'    //����

////////////////////////////////////////////////////////////////////////
///�����������
////////////////////////////////////////////////////////////////////////
#define THOST_FTDC_COMBT_Future '0'     //�ڻ����
#define THOST_FTDC_COMBT_BUL '1'        //��ֱ�۲�BUL
#define THOST_FTDC_COMBT_BER '2'        //��ֱ�۲�BER
#define THOST_FTDC_COMBT_STD '3'        //��ʽ���
#define THOST_FTDC_COMBT_STG '4'        //���ʽ���
#define THOST_FTDC_COMBT_PRT '5'        //�������
#define THOST_FTDC_COMBT_CLD '6'        //ʱ��۲����


/////////////////////////////////////////////////////////////////////////
///TFtdcExchangeIDType��һ����������������
/////////////////////////////////////////////////////////////////////////
typedef char TThostFtdcExchangeIDType[9];
/////////////////////////////////////////////////////////////////////////
///TFtdcExchangeInstIDType��һ����Լ�ڽ������Ĵ�������
/////////////////////////////////////////////////////////////////////////
typedef char TThostFtdcExchangeInstIDType[31];
/////////////////////////////////////////////////////////////////////////
///TFtdcSettlementGroupIDType��һ���������������
/////////////////////////////////////////////////////////////////////////
typedef char TThostFtdcSettlementGroupIDType[9];
/////////////////////////////////////////////////////////////////////////
///TFtdcInstrumentIDType��һ����Լ��������
/////////////////////////////////////////////////////////////////////////
typedef char TThostFtdcInstrumentIDType[31];
/////////////////////////////////////////////////////////////////////////
///TFtdcInstrumentStatusType��һ����Լ����״̬����
/////////////////////////////////////////////////////////////////////////
///����ǰ
#define THOST_FTDC_IS_BeforeTrading '0'
///�ǽ���
#define THOST_FTDC_IS_NoTrading '1'
///��������
#define THOST_FTDC_IS_Continous '2'
///���Ͼ��۱���
#define THOST_FTDC_IS_AuctionOrdering '3'
///���Ͼ��ۼ۸�ƽ��
#define THOST_FTDC_IS_AuctionBalance '4'
///���Ͼ��۴��
#define THOST_FTDC_IS_AuctionMatch '5'
///����
#define THOST_FTDC_IS_Closed '6'

typedef char TThostFtdcInstrumentStatusType;
/////////////////////////////////////////////////////////////////////////
///TFtdcTradingSegmentSNType��һ�����׽׶α������
/////////////////////////////////////////////////////////////////////////
typedef int TThostFtdcTradingSegmentSNType;
/////////////////////////////////////////////////////////////////////////
///TFtdcTimeType��һ��ʱ������
/////////////////////////////////////////////////////////////////////////
typedef char TThostFtdcTimeType[9];
///TFtdcInstStatusEnterReasonType��һ��Ʒ�ֽ��뽻��״̬ԭ������
/////////////////////////////////////////////////////////////////////////
///�Զ��л�
#define THOST_FTDC_IER_Automatic '1'
///�ֶ��л�
#define THOST_FTDC_IER_Manual '2'
///�۶�
#define THOST_FTDC_IER_Fuse '3'

typedef char TThostFtdcInstStatusEnterReasonType;


#pragma pack(push,1)
//1.1 �н����ڻ�����
typedef struct t_CFFEX_FutursMarketData {
	T_I32 nTime;                        //ʱ��(HHMMSSmmmm)
	T_I32 nStatus;                      //״̬
	T_I64 iPreOpenInterest;             //��ֲ�
	T_U32 uPreClose;                    //�����̼�
	T_U32 uPreSettlePrice;              //�����
	T_U32 uOpen;                        //���̼�
	T_U32 uHigh;                        //��߼�
	T_U32 uLow;                         //��ͼ�
	T_U32 uMatch;                       //���¼�
	T_I64 iVolume;                      //�ɽ�����
	T_I64 iTurnover;                    //�ɽ��ܽ��
	T_I64 iOpenInterest;                //�ֲ�����
	T_U32 uClose;                       //������
	T_U32 uSettlePrice;                 //�����
	T_U32 uHighLimited;                 //��ͣ��
	T_U32 uLowLimited;                  //��ͣ��
	T_I32 nPreDelta;                    //����ʵ��
	T_I32 nCurrDelta;                   //����ʵ��
	T_U32 uAskPrice[5];                 //������
	T_U32 uAskVol[5];                   //������
	T_U32 uBidPrice[5];                 //�����
	T_U32 uBidVol[5];                   //������
} Futures_MarketData, T_CFFEX_FutursMarketData, *PCFFEX_FutursMarketData;

//1.2 �н����ڻ�����Ȩ������Ϣ
typedef struct t_CFFEX_BaseInfo {
  char sInstrumentID[31];               //��Լ����
  char sExchangeID[9];                  //����������
  char sInstrumentName[21];             //��Լ����
  char sExchangeInstID[31];             //��Լ�ڽ������Ĵ���
  char sProductID[31];                  //��Ʒ����
  char cProductClass;                   //��Ʒ����
  T_I32 nDeliveryYear;                  //�������
  T_I32 nDeliveryMonth;                 //������
  T_I32 nMaxMarketOrderVolume;          //�м۵�����µ���
  T_I32 nMinMarketOrderVolume;          //�м۵���С�µ���
  T_I32 nMaxLimitOrderVolume;           //�޼۵�����µ���
  T_I32 nMinLimitOrderVolume;           //�޼۵���С�µ���
  T_I32 nVolumeMultiple;                //��Լ��������
  T_I64 i64PriceTick;                   //��С�䶯��λ,����10000��
  T_I32 nCreateDate;                    //������
  T_I32 nOpenDate;                      //������
  T_I32 nExpireDate;                    //������
  T_I32 nStartDelivDate;                //��ʼ������
  T_I32 nEndDelivDate;                  //����������
  char cInstLifePhase;                  //��Լ��������״̬
  T_I32 nIsTrading;                     //��ǰ�Ƿ���
  char cPositionType;                   //�ֲ�����
  char cPositionDateType;               //�ֲ���������
  T_I64 i64LongMarginRatio;             //��ͷ��֤����,������10000��
  T_I64 i64ShortMarginRatio;            //��ͷ��֤����,������10000��
  char cMaxMarginSideAlgorithm;         //�Ƿ�ʹ�ô��߱�֤���㷨
  char sUnderlyingInstrID[31];          //������Ʒ����
  T_I64 i64StrikePrice;                 //ִ�м�,������10000��
  char cOptionsType;                    //��Ȩ����
  T_I64 i64UnderlyingMultiple;          //��Լ������Ʒ����,������10000��
  char cCombinationType;                //�������
} T_CFFEX_BaseInfo,*PCFFEX_BaseInfo;


///���������̵�ѯ������
typedef struct t_CFFEX_ForQuote {
  T_I32 nTradingDay;                    //������
  char sInstrumentID[31];               //��Լ����
  char sForQuoteSysID[21];              //ѯ�۱��
  T_I32 nForQuoteTime;                  //ѯ��ʱ��
  int nActionDay;                       //ҵ������
  char sExchangeID[9];                  //����������
}T_CFFEX_ForQuote,*PCFFEX_ForQuote,T_ForQuote;


///��ԼƷ�ֽ���״̬
typedef struct t_CFFEX_INSTRUMENT_STATUS{
	///����������
	TThostFtdcExchangeIDType	ExchangeID;
	///��Լ�ڽ������Ĵ���
	TThostFtdcExchangeInstIDType	ExchangeInstID;
	///���������
	TThostFtdcSettlementGroupIDType	SettlementGroupID;
	///��Լ����
	TThostFtdcInstrumentIDType	InstrumentID;
	///��Լ����״̬
	TThostFtdcInstrumentStatusType	InstrumentStatus;
	///���׽׶α��
	TThostFtdcTradingSegmentSNType	TradingSegmentSN;
	///���뱾״̬ʱ��
	TThostFtdcTimeType	EnterTime;
	///���뱾״̬ԭ��
	TThostFtdcInstStatusEnterReasonType	EnterReason;
}T_CFFEX_INSTRUMENT_STATUS, *PCFFEX_INSTRUMENT_STATUS, T_INSTRUMENT_STATUS;

#pragma pack(pop)
#endif //_T_CFFEX_MARKET_