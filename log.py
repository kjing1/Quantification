# python 3.7.4
# coding = utf-8
# filename log.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2019/12/30

import logging
import os


def init_logging(logto, level):
    """
    初始化logging
    :param logto: 日志记录的文件
    :param level: 日志级别（info，warning，warn，debug）
    :return: logger
    """
    if level.lower() == 'debug':
        l = logging.DEBUG
    elif level.lower() == 'warning':
        l = logging.WARNING
    elif level.lower() == 'warn':
        l = logging.WARN
    elif level.lower() == 'error':
        l = logging.ERROR
    else:
        l = logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(level=l)
    handler = logging.FileHandler(os.path.expanduser(logto))
    handler.setLevel(level=l)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
