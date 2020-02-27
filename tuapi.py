# python 3.7.4
# coding = utf-8
# filename tuapi.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

import tushare as ts
import time
from utils import MyRetry

MYTOKEN = '7b5e2feb802bd4225de18e78e7b16e7fca8d03881a3d8707cf59e6be'


def tu_init(token):
    ts.set_token(token)
    pro = ts.pro_api()
    return pro


# 获取24H快讯
@MyRetry()
def tu_falsh_news(pro, src, start, end):
    df = pro.news(src=src, start_date=start, end_date=end, fields='title,content,datetime,channels')
    return df


# 获取长篇新闻
@MyRetry()
def tu_major_news(pro, src, start, end):
    df = pro.major_news(src=src, start_date=start, end_date=end, fields='title,content,pub_time,src')
    return df
