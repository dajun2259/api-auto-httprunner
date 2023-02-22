#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : setting.py
# @Author: 尘心2259
# @Date  : 2022/6/1 00:36
# @Desc  :
import os


class Path:
    """
        根路径
    """

    _SLASH = os.sep
    # 项目路径
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + _SLASH

    # 用例路径
    case_path = os.path.join(root_path, 'testcases' + _SLASH)
    # 测试用例数据路径
    data_path = os.path.join(root_path, 'data' + _SLASH)

    logs_path = os.path.join(root_path, 'logs' + _SLASH)

    # 测试报告路径
    report_path = os.path.join(root_path, 'report' + _SLASH)
    if not os.path.exists(report_path):
        os.makedirs(report_path
                    )
    # common路径
    common_path = os.path.join(root_path, "common" + _SLASH)

    # har路径
    har_path = os.path.join(root_path, 'har' + _SLASH)

    # attach路径
    attach_path = os.path.join(root_path, 'attach' + _SLASH)


if __name__ == '__main__':
    print(Path.common_path)
