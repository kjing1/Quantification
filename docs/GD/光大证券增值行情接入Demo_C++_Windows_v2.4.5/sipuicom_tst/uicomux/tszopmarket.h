
#ifndef _T_SZOPMARKET_H__
#define _T_SZOPMARKET_H__
#include "tdef.h"
//////////////////////////////////////////////////////////////////////////
//�����Ȩ����
//////////////////////////////////////////////////////////////////////////

#define  SZOP                 11    //�����Ȩ

#define ID_SZOP_BASEINFO      1     //��Ȩ������Ϣ
#define ID_SZOP_MARKETDATA    2     //��Ȩ��������

#pragma pack(push,1)
//////////////////////////////////////////////////////////////////////////
//�������֤ȯ���빲��  securities_YYYYMMDD.xml
typedef struct t_BaseInfo {
  char sSecurityID[8];              //֤ȯ���� SecurityID C8
  char sSymbol[40];                 //֤ȯ��� C40
  char sEnglishName[40];            //Ӣ�ļ�� ������Ȩ��д��Լ���� C40
  char sISIN[12];                   //ISIN���� C12
  char sSecurityIDSource[4];        //֤ȯ����Դ 4=ISIN 102=����֤ȯ������ C4
  char sUnderlyingSecurityID[8];    //����֤ȯ���� C8
  T_U32 uListDate;                  //�������� N8
  T_U16 usSecurityType;             //֤ȯ��� N4
  char sCurrency[4];                //���Ҵ��� C4
  T_I64 i64QtyUnit;                 //������λ ί�������ֶα���Ϊ��֤ȯ������λ�������� N15(2) �˴����ʹ����Ŵ�10000��
  char cDayTrading;                 //�Ƿ�֧�ֵ��ջ�ת���� Y=֧�� N=��֧�� C1
  T_I64 i64PrevClosePx;             //�������̼� N13(4)
  char sSecurityStatus[20];         //
  T_I64 i64OutstandingShare;        //�ܷ�����  N18(2)
  T_I64 i64PublicFloatShareQuantity;//��ͨ���� N18(2)
  T_I64 i64ParValue;                //��ֵ N13(4)
  char cGageFlag;                   //�Ƿ����ҵ������ȯ�ɳ�ֱ�֤��֤ȯ C1  Y=�� N=��
  T_I32 nGageRatio;                 //�ɳ�ֱ�֤�������� N5(2)
  char cCrdBuyUnderlying;           //�Ƿ�Ϊ���ʱ�� C1 Y=�� N=��
  char cCrdSellUnderlying;          //�Ƿ�Ϊ��ȯ���C1 Y=�� N=��
  char cPledgeFlag;                 //�Ƿ����Ѻ��� C1 Y=�� N=��
  T_I32 nContractMultiplier;        //�Իع���׼ȯ������ N6(5)
  char sRegularShare[8];            //��Ӧ�ع���׼ȯ C8
} T_BASEINFO,*PBASEINFO;

//////////////////////////////////////////////////////////////////////////
//��Ȩ�����ֶ�   securities_YYYYMMDD.xml
typedef struct t_OptionParams {
  char cCallOrPut;                  //�Ϲ����Ϲ� C1 C=Call P=Put
  T_I32 nDeliveryDay;               //��������  N8
  char cDeliveryType;               //���ʽ C1  S=֤ȯ���� C=�ֽ����
  T_I32 nExerciseBeginDate;         //��Ȩ��ʼ���� N8
  T_I32 nExerciseEndDate;           //��Ȩ�������� N8
  T_I64 i64ExercisePrice;           //��Ȩ�� N13(4)
  char cExerciseType;               //��Ȩ��ʽ C1 A=��ʽ E=ŷʽ B=��Ľ��ʽ
  T_I32 nLastTradeDay;              //������� N8
  //char          cAdjusted;//�Ƿ���� C1 Y=�� N=��
  T_U16 usAdjustTimes;              //�������� N2
  T_I64 i64ContractUnit;            //��Լ��λ N15(2)
  T_I64 i64PrevClearingPrice;       //���ս���� N13(4)
  T_I64 i64ContractPosition;        //��Լ�ֲ���  N18(2)
} T_OPTIONPARAMS,*POPTIONPARAMS;

//����Ʒ�ο���Ϣ��Ŀǰ��������Ȩ  derivativeauctionparams_YYYYMMDD.xml

typedef struct t_DerivativeParams {
  char sSecurityID[8];              //֤ȯ���� C8
  T_I64 i64BuyQtyUpperLimit;        //��ί���������� N15(2)
  T_I64 i64SellQtyUpperLimit;       //��ί���������� N15(2)
  T_I64 i64BuyQtyUnit;              //��������λ N15(2)
  T_I64 i64SellQtyUnit;             //��������λ N15(2)
  T_I64 i64PriceTick;               //�۸�λ N13(4)
  T_I64 i64PriceUpperLimit;         //��ͣ�� N13(4)
  T_I64 i64PriceLowerLimit;         //��ͣ�� N13(4)
  T_I64 i64LastSellMargin;          //��־��ÿ�ű�֤�� N18(4)
  T_I64 i64SellMargin;              //������ÿ�ű�֤�� N18(4)
  T_I32 nMarginRatioParam1;         //��֤������������һ N4(2)
  T_I32 nMarginRatioParam2;         //��֤������������һ N4(2)
  char cMarketMakerFlag;            //�����̱�־  C1 Y=�� N=��
} T_DERIVATIVEPARAMS,*PDERIVATIVEPARAMS;


typedef struct t_SZOP_BaseInfo {
  T_BASEINFO tBase;                 //������Ϣ
  T_OPTIONPARAMS tOpParams;         //��Ȩ����
  T_DERIVATIVEPARAMS tDeParmas;     //����Ʒ��Ϣ

} T_SZOP_BASEINFO,*PSZOP_BASEINFO;  //ID_SZOP_BASEINFO

typedef struct t_SZOP_MarketData {
  T_I32 nTime;                      //��������ʱ�� HHMMSSmmm��ʽ
  T_U16 usChannelNo;                //Ƶ������
  char sMDStreamID[3];              //�������
  char sSecrityID[8];               //֤ȯ����
  char sSecurityIDSource[4];        //֤ȯ����Դ 101=����֤ȯ������
  char sTradingPhaseCode[8];        //��Ʒ�����Ľ��׽׶δ��� ��0λ��S=����������ǰ�� O=���̼��Ͼ��� T=�������� B=���� C=���̼��Ͼ��� E=�ѱ��� H=��ʱͣ�� A=�̺��� ��1λ��0=����״̬ 1=ȫ��ͣ��
  T_I64 i64PrevClosePx;             //���ռ�
  T_I64 i64NumTrades;               //�ɽ�����
  T_I64 i64TotalVolumeTrade;        //�ɽ�����
  T_I64 i64TotalValueTrade;         //�ɽ��ܽ��

  T_I64 i64LastPrice;               //�����
  T_I64 i64OpenPrice;               //���̼�
  T_I64 i64HighPrice;               //��߼�
  T_I64 i64LowPrice;                //��ͼ�
  T_I64 i64BuyAvgPrice;             //x3=������ܣ���������Ȩƽ���ۣ�
  T_I64 i64BuyVolumeTrade;          //x3=������ܣ���������Ȩƽ���ۣ�
  T_I64 i64SellAvgPrice;            //x4=�������ܣ���������Ȩƽ���ۣ�
  T_I64 i64SellVolumeTrade;         //x4=�������ܣ���������Ȩƽ���ۣ�
  T_I64 i64OfferPrice[10];          //��ί�м۸�
  T_I64 i64OfferQty[10];            //��ί����
  T_I64 i64BidPrice[10];            //��ί�м۸�
  T_I64 i64BidQty[10];              //��ί����
  T_I64 i64PriceUpperLimit;         //��ͣ��
  T_I64 i64PriceLowerLimit;         //��ͣ��
  T_I64 i64ContractPosition;        //��Լ�ֲ���


  //������Ŀ��� 0=���� 1=���� 2=����� 4=���̼� 7=��߼� 8=��ͼ�
  //x1= ����һ x2=������ x3=������ܣ���������Ȩƽ���ۣ�x4=�������ܣ���������Ȩƽ���ۣ�
  //x5=��Ʊ��ӯ��һ x6=��Ʊ��ӯ�ʶ� x7=����T-1�վ�ֵ x8=����ʵʱ�ο���ֵ(����ETF��IOPV)
  //x9=Ȩ֤����� xe=��ͣ�� xf=��ͣ�� xg=��Լ�ֲ���
} T_SZOP_MARKETDATA,*PSZOP_MARKETDATA;

#pragma pack(pop)
#endif // _T_SZOPMARKET_H__