# python 3.7.4
# coding = utf-8
# filename news.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

import tushare as ts
import dbpool
import time
from utils import logto

token = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'
# 初始化tushare
ts.set_token(token)
PRO = ts.pro_api()
LOGFILE = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\log_news.txt'
CHANNEL = ['sina', 'wallstreetcn', '10jqka', 'eastmoney', 'yuncaijing']
DATELIST = ['2020-02-01', '2020-02-02', '2020-02-03', '2020-02-04', '2020-02-05',
            '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10', '2020-02-11',
            '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-15', '2020-02-16', '2020-02-17',
            '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21']


def get_channel_chname(c):
    if c == 'sina':
        return '新浪财经'
    elif c == 'wallstreetcn':
        return '华尔街见闻'
    elif c == '10jqka':
        return '同花顺'
    elif c == 'eastmoney':
        return '东方财富'
    elif c == 'yuncaijing':
        return '云财经'
    else:
        return c


def get_flash_news(src, start, end, maxretry=5):
    count = 1
    while True:
        try:
            df = PRO.news(src=src, start_date=start, end_date=end, fields='title,content,datetime,channels')
        except Exception as e:
            logto(LOGFILE, 'Get news from %s to %s failure: %s, retry: %d-%d\n'
                  % (start, end, e, count, maxretry))
            if count <= maxretry:
                count += 1
                continue
            else:
                return None
        else:
            return df


def get_major_news(src, start, end, maxretry=5):
    count = 1
    while True:
        try:
            df = PRO.major_news(src=src, start_date=start, end_date=end, fields='title,content,pub_time,src')
        except Exception as e:
            logto(LOGFILE, 'Get major news from %s to %s failure: %s, retry: %d-%d\n'
                  % (start, end, e, count, maxretry))
            if count <= maxretry:
                count += 1
                continue
            else:
                return None
        else:
            return df


if __name__ == '__main__':
    # 链接数据库
    conn = dbpool.MyPymysqlPool('MysqlDatabaseInfo-news')

    """
    # 获取快讯
    for c in CHANNEL:
        # 获取2020年1月和2月的所有快讯
        for d in DATELIST:
            df = get_flash_news(src=c, start='%s 00:00:00' % d, end='%s 23:59:59' % d)
            if df is not None:
                for key, val in df.iterrows():
                    try:
                        cls = '%s' % val['channels'][0]['name']
                    except Exception as e:
                        cls = '其他'
                    sql = 'INSERT INTO s_flash_news (type, source, creat_date, content, pub_datetime) VALUES (' \
                          '"%s", "%s", "%s", "%s", "%s")' % (cls,
                                                             get_channel_chname(c),
                                                             time.time(),
                                                             val['content'].replace("\\", "\\\\").replace("'",
                                                                                                          "\\'").replace(
                                                                 '"', '\\"'),
                                                             val['datetime'])
                    if conn.insert(sql) == 1:
                        print('GET_FLASH_NEWS record:%d insert successful' % key)
                    else:
                        print('GET_FLASH_NEWS record:%d insert failure' % key)
                        logto(LOGFILE, 'GET_FLASH_NEWS record:%d insert failure, SQL: %s\n' % (key, sql))
                conn.end(option='commit')
    """

    # 获取长篇新闻
    for d in DATELIST:
        df = get_major_news(src='', start='%s 00:00:00' % d, end='%s 23:59:59' % d)
        if df is not None:
            for key, val in df.iterrows():
                sql = 'INSERT INTO s_major_news (title, type, source, creat_date, content, pub_datetime) VALUES (' \
                      '"%s", %s, "%s", "%s", "%s", "%s")' % (val['title'],
                                                             '新闻',
                                                             val['src'],
                                                             time.time(),
                                                             val['content'].replace("\\", "\\\\").replace("'","\\'").replace('"', '\\"'),
                                                             val['pub_time'])
                if conn.insert(sql) == 1:
                    print('GET_MAJOR_NEWS record:%d insert successful' % key)
                else:
                    print('GET_MAJOR_NEWS record:%d insert failure' % key)
                    logto(LOGFILE, 'GET_FLASH_NEWS record:%d insert failure, SQL: %s\n' % (key, sql))
            conn.end(option='commit')

    conn.dispose()
