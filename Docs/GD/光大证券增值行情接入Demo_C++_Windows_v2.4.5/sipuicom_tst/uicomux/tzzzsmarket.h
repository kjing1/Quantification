
#ifndef _T_ZZZS_MARKET_
#define _T_ZZZS_MARKET_
#include "tdef.h"
#pragma pack(push,1)

//�г�����
#define ZZZS                7     //��ָ֤�������г�

#define  ID_ZZZS_INDEX      0x01  //��ָ֤������ ��ӦT_ZZZS_IndexMarketData
#define  ID_ZZZS_WEIGHT     0x02  //Ȩ����Ϣ ��ӦT_ZZZS_IndexWeight
#define  ID_ZZZS_ETFIOPV    0x03  //ETF��IOPV ��ӦT_ZZZS_EtfIopv


//1.1 ָ��������Ϣ
typedef struct t_ZZZS_IndexMarketData {
  T_U16 nRecordType;              //��¼���ͣ�01��ָ��������Ϣ��02��ָ��Ȩ����Ϣ��03��ETF��IOPV���ο���ֵ��  ��ӦJLLX
  T_I32 nTime;                    //ʱ�� HHMMSSmmm
  char szStandby[5];              //�����ֶΣ�ȫ���ÿո����     
  char szIndexCode[7];            //ָ������  ��ӦZSDM
  char szIndexReferred[21];       //ָ�����  ��ӦJC
  T_U16 nMarketCode;              //�г����� 1:��֤����2:�����3:���4:��ۡ�5:��̫��0:ȫ�� ��ӦSCDM
  T_U64 iRealtimeIndex;           //ʵʱָ������ǰָ��ֵ ��ӦSSZS                    �Ŵ�1w��
  T_U64 iOpenValueOfToday;        //���տ���ֵ����ʼΪ0.0000������Ϊ0.0000��ʾδ���̡�  ��ӦDRKP  �Ŵ�1w��
  T_U64 iMaximumOfDay;            //�������ֵ����ǰ���������ָ��ֵ��  ��ӦDRZD          �Ŵ�1w��
  T_U64 iMinimumOfDay;            //������Сֵ����ǰ��������Сָ��ֵ��  ��ӦDRZX          �Ŵ�1w��
  T_U64 iCloseValueOfToday;       //��������ֵ����ʼΪ0.0000�����䲻Ϊ0.0000��ʾ�����̡�  ��ӦDRSP  �Ŵ�1w��
  T_U64 iCloseValueOfYesterday;   //��������ֵ����һ�����յ�����ֵ��  ��ӦZRSP            �Ŵ�1w��
  T_I64 iRiseAndFall;             //�ǵ�  ��ӦZD                            �Ŵ�1w��
  T_I64 iRiseAndFallRange;        //�ǵ���  ��ӦZDF                          �Ŵ�1w��
  T_U64 iMatchVolume;             //�ɽ�����λΪ�ɣ������ծȯָ����λΪ�š�  ��ӦCJL        
  T_U64 iMatchAmount;             //�ɽ�����λΪ��Ԫ  ��ӦCJJE                  �Ŵ�10w��
  T_U64 iExchangeRate;            //���ʣ�����Ϊ0.00000000.���̺�Ϊ����ʱ����ָ����ʹ�õĻ���  ��ӦHL  �Ŵ�1�ڱ�
  T_U16 nMoneyType;               //�������ࡣ0������ң�1���۱ң�2���� Ԫ ��3��̨�ң�4����Ԫ  ��ӦBZBZ
  T_U32 nIndexSerial;             //ָ��չʾ��� ��ӦZSXH
  T_U64 iCloseValueOfToday2;      //��������ֵ2������ָ��Ϊȫ��ָ����������ֵΪ������̫������ֵ��
                                  //��ʼֵΪ0.0000����ֵ��Ϊ0.0000ʱ��˵��ָ����̫�������̡���ӦDRSP2 �Ŵ�1w��
  T_U64 iCloseValueOfToday3;      //��������ֵ3������ָ��Ϊȫ��ָ����������ֵΪ����ŷ��������ֵ��
                                  //��ʼֵΪ0.0000����ֵ��Ϊ0.0000ʱ��˵��ָ��ŷ���������̡���ӦDRSP3 �Ŵ�1w��


} T_ZZZS_IndexMarketData, *PZZZS_IndexMarketData;

//1.2 ָ��Ȩ����Ϣ�ṹ��
typedef struct t_ZZ_IndexWeight {
  T_U16 nRecordType;              //��¼���ͣ�01��ָ��������Ϣ��02��ָ��Ȩ����Ϣ��03��ETF��IOPV���ο���ֵ��  ��ӦJLLX
  T_I32 nTime;                    //ʱ�� HHMMSSmmm
  char szStandby[5];              //�����ֶΣ�ȫ���ÿո����     
  char szIndexCode[7];            //ָ������  ��ӦZSDM
  char szIndexName[21];           //ָ������  ��ӦZSMC
  char szStockCode[9];            //֤ȯ����  ��ӦZQDM
  char szStockName[9];            //֤ȯ����  ��ӦZQMC
  T_U64 iWeightRate;              //Ȩ�ر�  ��ӦQZ                      �Ŵ�10w��
  T_U64 iCurrentIndexValue;       //��ǰָ��ֵ ��ӦDQZS                    �Ŵ�1w��
  T_I64 iImpactPointNumerical;    //Ӱ�����ֵ  �ù�Ʊ�ڵ�ǰʱ���ָ���Ĺ��׵��� ��ӦYXDS    �Ŵ�1w��

} T_ZZZS_IndexWeight, *PZZZS_IndexWeight;

//1.3 ETF��IOPV��ֵ
typedef struct t_ZZZS_EtfIopv {
  T_U16 nRecordType;              //��¼���ͣ�01��ָ��������Ϣ��02��ָ��Ȩ����Ϣ��03��ETF��IOPV���ο���ֵ��  ��ӦJLLX
  T_I32 nTime;                    //ʱ�� HHMMSSmmm
  char szStandby[5];              //�����ֶΣ�ȫ���ÿո����     
  char szStockCode[9];            //ETF��֤ȯ����  ��ӦZQDM
  char szStockName[9];            //ETF��֤ȯ����  ��ӦZQMC
  T_U16 nMarketCode;              //�г����� 1:��֤����2:�����3:���4:��ۡ�5:��̫��0:ȫ�� ��ӦSCDM
  T_I64 iIOPV;                    //����ο���ֵ��IOPV��  ��ӦIOPV              �Ŵ�1w��
} T_ZZZS_EtfIopv, *PZZZS_EtfIopv;

#pragma pack(pop)

#endif //_T_ZZZS_MARKET_