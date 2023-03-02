#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project : api_auto_test
# @File    : txt_utils.py
# @Time    : 2023-02-02 17:59:18
# @User    : cx2259
# @Author  : chen xin
# @Description :
import traceback

from utils.log.loguru_utils import Logger


def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        Logger().error(traceback.format_exc())


def write_txt(file_path, text):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        Logger().error(traceback.format_exc())


if __name__ == '__main__':
    a = read_txt("/Users/cx2259/project/api/api_auto_httprunner/utils/file_utils/txt_utils.py")
    print(a)
