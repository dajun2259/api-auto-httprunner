#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project : api_auto_test
# @File    : time_utils.py
# @Time    : 2023-01-30 16:15:42
# @User    : cx2259
# @Author  : chen xin
# @Description :
import time


def time_to_stamp(times):
    s_t = time.strptime(times, "%Y-%m-%d %H:%M:%S")  # 返回元组
    return str(int(time.mktime(s_t))) + "000"


if __name__ == '__main__':
    a = time_to_stamp("2023-02-11 16:00:00")
    print(a)