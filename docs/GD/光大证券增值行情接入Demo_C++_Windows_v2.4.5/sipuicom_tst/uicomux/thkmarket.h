#ifndef _T_HKMARKET_H_ 
#define _T_HKMARKET_H_

#pragma warning (disable : 4996 4200)
#include "tdef.h"

#define HK                   9             //����г�

#define ID_HK_ORGMSG         1             // ԭʼOMD��Ϣ���ݣ���Ҫ�����ڴ�洢��ÿ��֤ȯ����2��ҳ��
#define ID_HK_EXMSG          2             // ��չ��Ϣ��10�����飬Ŀǰֻ�� ��Ϣ��Ϊ90 ����Ϣ(10������),�������һ����Ҳ��Ҫ�����ڴ�洢
#define ID_HK_CUR            3             // ���� ��Ӧomd 14
#define ID_HK_INDEX          4             // ָ�� ��Ӧomd 71
#define ID_HK_BASEINFO       5             // ������Ϣ ��Ӧomd 11
#define ID_HK_COUNT          6             // ͳ��  ��Ӧ omd 60
#define ID_HK_CLOSEPRICE     7             // ���̼� ��Ӧ omd 62
#define ID_HK_EXMSGL1        8             // ��չ��Ϣ ��Ϣ��91 5������

#pragma pack(push,1)

// 3.3 PACKET HEADER ����ͷ--------------------------------
typedef struct t_omdpacket {
  T_U16 usPkgSize;                         //���ĳ��ȣ���������ͷ
  T_U8 ucMsgCout;                          //��Ϣ����
  T_U8 ucFiller1;                          //��� 
  T_U32 uSeqNum;                           //��һ����Ϣ�����
  T_U64 ulSendTime;                        //����ʱ�䣬��1970-1-1 0��0��0 GMTʱ�꣬��λ����
  T_U8 pdata[];
} OMD_PACKET, *POMDPACKET;                 // sizeof() = 16

// OMD��Ϣͨ�ø�ʽ             
typedef struct t_omdmsg {
  T_U16  usMsgSize;                        //��Ϣ����
  T_U16  usMsgType;                        //��Ϣ����
  T_U8  pdata[];
} OMD_MSG, *POMDMSG;                       // sizeof() = 4

// 3.7.2 Security Definition (11) ֤ȯ������Ϣ-----------------
typedef struct t_securitydefine {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(11)
  T_U32 uSecurityCode;                     //֤ȯ����,1-99999��5λʮ����
  char sMarketCode[4];                     //�г�����,MAIN,GEM,NASD,ETS,ע��ĩβ����û��0�ַ�
  char sISINCode[12];                      //ISIN����,֤ȯ���ʴ���.
  char sInstrumentType[4];                 // BOND(ծȯ),BWRT(����Ȩ֤),EQTY(��Ʊ),TRST(����),WRNT(Ȩ֤)
  char sSpreadTableCode[2];                // '01' PArtA , '02' PartB
  char sSecurityShortName[40];             // ֤ȯ����
  char sCurrencyCode[3];                   // ���Ҵ���,HKD,USD,EUR,JPY,GBP,CAD,SGD,CNY
  T_U8 usGCCSName[60];                     // ������ķ���UnicodeUTF-16LE����
  T_U8 usGBName[60];                       // GB����UnicodeUTF-16LE����
  T_U32 uLotSize;                          // ������λ��Board lot size for the security
  T_I32 iPrelosePrice;                     // ǰ���м�
  char cFiller1;                           // res1
  char cShortSellFlag;                     // Y Short-sell allowed,N Short-sell not allowed
  char cFiller2;                           // res2
  char cCCASSFlag;                         // Y CCASS security,N Non CCASS security
  char cDummySecurityFlag;                 // Y Dummy security,N Normal security
  char cTestSecurityFlag;                  // Y Test security,N Normal security
  char cStampDutyFlag;                     // Y Stamp duty required,N Stamp duty not required
  char cFiller3;                           // res3
  T_U32 uListingDate;                      // �������� YYYYMMDD,19000101 ��ʾδ֪
  T_U32 uDelistingDate;                    // �������� YYYYMMDD,0 ��ʾδ֪
  char sFreeText[38];                      // �̶����ȵ�FreeText,���û�У���д�ո�
  char cEFNFlag;                           // Y EFN,N Non-EFN
  T_U32 uAccruedInterest;                  // Accrued Interest,Լ��3λС��
  T_U32 uCouponRate;                       // Coupon Rate,Լ��3λС��
  T_U32 uConversionRatio;                  // Conversion Ratio,Լ��3λС��
  T_I32 iStrikePrice;                      // Strike Price��Ȩ�ۣ�Լ��3λС��
  T_U32 uMaturityDate;                     // �����գ�YYYYMMDD
  char cCallPutFlag;                       // Derivative Warrants/Basket: C Call,P Put
                                           // ELI & CBBC: C Bull,P Bear / Rang
  char cStyle;                             // Style of the basket warrant:A American style,E European style,<blank> Other
  T_U16 usNoUnderlyingSecurities;          // 0 to 20 for Basket Warrants;0 to 1 for Warrants and Structured Product
  struct t_uls{
    T_U32 uUnderlyingSecurityCode;         // 5-digit code identifying the underlying security.
    T_U32 uUnderlyingSecurityWeight;       //The weight of the underlying security code.
  } uls[];
} OMDMSG_SECURITYDEFINE;                   // sizeof() = 280 + 8*nu   (nu = usNoUnderlyingSecurities)

// 3.7.4 Currency Rate (14) ����---------------------------
typedef struct  t_currencyrate {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(14)
  char sCurrencyCode[3];                   //���Ҵ���,HKD,USD,EUR,JPY,GBP,CAD,SGD,CNY
  char cFiller;      
  T_U16 usCurrencyFactor;                  // ��0��ʾ�۸����10 n�η�
  char sFiller[2];
  T_U32 uCurrencyRate;                     // HKD��ʾ����ҵ�λ��Լ��4λС��
} OMDMSG_CURRENCERATE;                     // sizeof() = 16

// 3.11.1 Statistics (60) ͳ��-----------------------------
typedef struct t_statistics {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(60)
  T_U32 uSecurityCode;                     //֤ȯ����,1-99999��5λʮ����
  T_U64 ulSharesTraded;                    //������(��)
  T_I64 lTurnover;                         //���׶�, Լ��3λС��
  T_I32 iHighPrice;                        //��߼ۣ�Լ��3λС��
  T_I32 iLowPrice;                         //��ͼۣ�Լ��3λС��
  T_I32 iLastPrice;                        //���ۣ�Լ��3λС��
  T_I32 iVWAP;                             //Volume-Weighted Average Price�ɽ�����Ȩƽ���۸�Լ��3λС��
  T_U32 uShortSellShares;                  //Number of short-sell shares���չ���
  T_I64 lShortSellTurnover;                //short-sell turnover���ճɽ���(���)��Լ��3λС��
} OMDMSG_STATISTICS;                       // sizeof() = 52

// 3.10.4 Closing Price (62) ���м�------------------------
typedef struct t_closeprice {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(62)
  T_U32 uSecurityCode;                     //֤ȯ����,1-99999��5λʮ����
  T_I32 iPrice;                            //���м۸�Լ��3λС��
  T_U32 uNumberOfTrades;                   //������,Total Number of Trades performed on the given instrument
} OMDMSG_CLOSEPRICE;                       //sizeof() = 16

// 3.13.2 Index Data (71) ָ������-------------------------
typedef struct t_indexdata {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(71)
  char sIndexCode[11];                     //Upstream source��s index code
  char cIndexStatus;                       //Index status.
                                           //C Closing value
                                           //I Indicative
                                           //O Opening index
                                           //P Last close value (prev. ses.)
                                           //R Preliminary close
                                           //S Stop loss index
                                           //T Real-time index value
  T_I64 lIndexTime;                        //��1970-1-1 0��0��0 GMTʱ�꣬��λ����  
  T_I64 lIndexValue;                       //4λС����Current value of the index
  T_I64 lNetChgPrevDay;                    //4λС����Net change in value from previous day��s closing value versus last index value 
  T_I64 lHighValue;                        //4λС��
  T_I64 lLowValue;                         //4λС��
  T_I64 lEASValue;                         //2λС��,Estimated Average Settlement Value
  T_I64 lIndexTurnover;                    //4λС��
  T_I64 lOpeningValue;                     //4λС��
  T_I64 lClosingValue;                     //4λС��
  T_I64 lPreviousSesClose;                 //4λС��,Previous session closing value
  T_I64 lIndexVolume;                      //4λС��,Index volume of underlying constituents.,Only applicable for CSI.
  T_I32 iNetChgPrevDayPct;                 //4λС��,Net change in percentage from previous day��s closing value versus last value
  char cException;                         //Exception indicator
                                           //# Index with HSIL defined exceptional rule applied
                                           //' ' Normal index (empty string)
  char sFiller[3];
} OMDMSG_INDEXDATA;                        //sizeof() = 112

// MsgType = 90 , ����OMD 53��Ϣ��ԭ��10������
#define OMD_LEVELS  10
typedef struct t_omdmsgex_level10 {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(90) ��չ��Ϣ
  T_U32 uSecurityCode;                     //֤ȯ����,1-99999��5λʮ����
                                         
  T_I64 ltime;                             // ʱ��OMD�ж����ʱ��,��1970-1-1 0��0��0 GMTʱ�꣬��λ����,0��ʾ������Ч
  T_I32 iPrelosePrice;                     // ǰһ�����̼ۣ�����11
  T_I32 iPrice;                            //���̼۸�Լ��4λС�� ,����40
                                         
  T_U64 ulSharesTraded;                    //������(��) ,����6������60
  T_I64 lTurnover;                         //���׶�,Լ��4λС��
  T_I32 iHighPrice;                        //��߼ۣ�Լ��4λС��
  T_I32 iLowPrice;                         //��ͼۣ�Լ��4λС��
  T_I32 iLastPrice;                        //���ۣ�Լ��4λС��
  T_I32 iVWAP;                             //Volume-Weighted Average Price�ɽ�����Ȩƽ���۸�Լ��3λС��

  //���°���53���
  T_I32 iPrice_b[OMD_LEVELS];
  T_U64 uQuantity_b[OMD_LEVELS];

  T_I32 iPrice_s[OMD_LEVELS];  
  T_U64 uQuantity_s[OMD_LEVELS];
} OMDMSGEX_LEVEL10,*POMDMSGEX_LEVEL10;     // sizeof() = 256

#define OMD_LEVEL1   5
typedef struct t_omdmsgex_level1 {
  T_U16 usMsgSize;                         //��Ϣ����
  T_U16 usMsgType;                         //��Ϣ����(91) ��չ��Ϣ
  T_U32 uSecurityCode;                     //֤ȯ����,1-99999��5λʮ����

  T_I64 ltime;                             // ʱ��OMD�ж����ʱ��,��1970-1-1 0��0��0 GMTʱ�꣬��λ����,0��ʾ������Ч
  T_I32 iPrelosePrice;                     // ǰһ�����̼ۣ�����11
  T_I32 iPrice;                            //���Ƽ۸�Լ��3λС�� ,����40

  T_U64 ulSharesTraded;                    //������(��) ,����6������60
  T_I64 lTurnover;                         //���׶�,Լ��4λС��
  T_I32 iHighPrice;                        //��߼ۣ�Լ��4λС��
  T_I32 iLowPrice;                         //��ͼۣ�Լ��4λС��
  T_I32 iLastPrice;                        //���ۣ�Լ��4λС��
  T_I32 iVWAP;                             //Volume-Weighted Average Price�ɽ�����Ȩƽ���۸�Լ��3λС��

  //����53���
  T_I32 iPrice_b[OMD_LEVEL1];
  T_U64 uQuantity_b[OMD_LEVEL1];

  T_I32 iPrice_s[OMD_LEVEL1];  
  T_U64 uQuantity_s[OMD_LEVEL1];
} OMDMSGEX_LEVEL1,*POMDMSGEX_LEVEL1; // sizeof() =  176

#pragma pack(pop)
#endif //_T_HKMARKET_H_