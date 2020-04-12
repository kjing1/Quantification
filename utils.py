# python 3.7.4
# # coding = utf-8
# # filename utils.py
# # author 463714869@qq.com/www.cdzcit.com,
# #        create by VIM at 2019/12/30

import arrow
import sys
import time
from typing import Any, Dict, List


def isLeapYear(years):
    """
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return days_sum: 一年的总天数
    """

    if (years % 4 == 0 and years % 100 != 0) or (years % 400 == 0):
        days_sum = 366
    else:
        days_sum = 365

    return days_sum


class RetryDecorator(object):
    def __init__(self, retry: int = 5, intv: int = 1) -> None:
        if retry > 0:
            self.max_retry_num = retry
        else:
            self.max_retry_num = sys.maxsize
        self.intv_ = intv

    def __call__(self, func) -> Any:
        def _wrapper(*args, **kwargs):
            cnt = 1
            while cnt <= self.max_etry_num:
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    cnt += 1
                    time.sleep(self.intv_)
                else:
                    return ret
            return None

        return _wrapper


def Retry(func, logger, retrynum, *args, **kwargs):
    def _isloop(n, m):
        if m <= 0:
            return True
        else:
            return n <= m
    cnt = 1
    logger.debug('Retry %d times, dest function: %s, ARGS: %s' % (retrynum, str(func), args))
    while _isloop(cnt, retrynum):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            logger.error('%s execute get error: %s. Retry %d times' % (str(func), e, cnt))
            cnt += 1
        else:
            logger.debug('All retry %d times, dest function: %s, ARGS: %s execute successful' % (cnt, str(func), args))
            return ret
    logger.error('%s all retry %d times, execute failure' % (str(func), cnt))
    return None


def funcRetry(func, retry, intv, *args, **kwargs):
    def _isloop(n, m):
        if m <= 0:
            return True
        else:
            return n <= m
    cnt = 1
    while _isloop(cnt, retry):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            cnt += 1
            if intv:
                time.sleep(intv)
        else:
            return ret
    return None


def getAllDayPerYear(years, n):
    """
    获取一年的所有日期
    :param years: 年份
    :return: 全部日期列表
    """
    print(n)

    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))

    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)

    return all_date_list
