# python 3.7.4
# coding = utf-8
# filename news.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from db import dbpool
import time
import log
import tus.api as tsapi

LOGFILE = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\logs\\log_news.txt'
CHANNEL = ['sina', 'wallstreetcn', '10jqka', 'eastmoney', 'yuncaijing']
TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))


if __name__ == '__main__':
    # 初始化日志
    logger = log.init_logging(LOGFILE, 'debug')
    # 链接数据库
    conn = dbpool.MyPymysqlPool(logger, 'MysqlDatabaseInfo-news')
    # 初始化tushare
    pro = tsapi.init_tushare(logger, tsapi.MYTOKEN)
    if pro is None:
        print('Init tushare error, exit')
        exit(1)

    # 获取快讯和长篇新闻
    for c in CHANNEL:
        ret = tsapi.insert_flash_news_to_db(logger, pro, conn, TODAY+' 00:00:00', TODAY+' 23:59:59', c, retry=-1)
        if ret > 0:
            print('%s : all %d news from %s insert to db' %
                  (time.strftime('%Y-%m-%d', time.localtime(time.time())), ret, tsapi.get_channel_chname(c)))
        else:
            print('%s : %s channel not found data or get some errors, see %s to more informations' %
                  (time.strftime('%Y-%m-%d', time.localtime(time.time())), tsapi.get_channel_chname(c), LOGFILE))

    # 获取长篇新闻
    ret = tsapi.insert_mojor_news_to_db(logger, pro, conn, TODAY+' 00:00:00', TODAY+' 23:59:59', '', retry=-1)
    if ret > 0:
        print('%s : all %d news insert to db' %
              (time.strftime('%Y-%m-%d', time.localtime(time.time())), ret))
    else:
        print('%s : not found data or get some errors, see %s to more informations' %
              (time.strftime('%Y-%m-%d', time.localtime(time.time())), LOGFILE))

    conn.dispose()
