# python 3.7.4
# coding = utf-8
# filename utils.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import arrow
import os
import functools
import logging


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


def logto(f, s):
    with open(os.path.expanduser(f), 'a') as wf:
        try:
            wf.write(s)
        except Exception as e:
            print('Write %s to %s failure, ignore.' % (s, f))


class MyRetry(object):
    def __init__(self, l='.\\log.txt', n=5):
        self.logfile = l
        self.max_retry_num = n

    def __call__(self, func):
        def _wrapper(*args, **kwargs):
            cnt = 1
            while cnt <= self.max_retry_num:
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    logto(self.logfile, 'Call->%s get exception: %s, retry: %d->%d\n' % (func.__name__, e, cnt, self.max_retry_num))
                    cnt += 1
                else:
                    return ret
            logto(self.logfile, 'Call->%s failure, All try %d times\n' % (func.__name__, cnt - 1))
            return None

        return _wrapper


def getAllDayPerYear(years):
    """
    获取一年的所有日期
    :param years: 年份
    :return: 全部日期列表
    """
    raise Exception('111')

    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))

    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)

    return all_date_list


if __name__ == '__main__':
    date_list = getAllDayPerYear("2020")
    if date_list is not None:
        print(date_list)
    else:
        print('Get None')
