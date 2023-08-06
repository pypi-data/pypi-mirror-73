# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log
   Description :
   Author :       艾登科技 Asdil
   date：          2020/7/9
-------------------------------------------------
   Change Activity:
                   2020/7/9:
-------------------------------------------------
"""
__author__ = 'Asdil'
from loguru import logger


def example():
    """example方法用于

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    # logger.add("somefile.log", rotation="1 MB", enqueue=True, level="INFO")  # 异步写入
    return 0
