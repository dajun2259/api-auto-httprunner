#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : har_py_utils.py
# @Author: 尘心2259
# @Date  : 2022/5/11 22:46
# @Desc  : 批量har目录的har文件转换为py文件，然后移动到testcases文件，需要考虑到已存在的文件


"""
1.先获取har目录的所有文件，判断是否为.har的文件，然后存在列表里，循环获取文件，通过har2case批量转换py文件

2.判断生成的文件格式是否为.py文件，如果testcases目录不存在该文件就移动
"""
import os
import shutil
import traceback

from common.setting import Path
from utils.file_utils.files_utils import get_all_files
from utils.loguru_utils import Logger


def har_convert_py_one(name):
    """

    :param name:
    :return:
    """

    try:
        har_dir = Path.har_path + name

        os.system(f"har2case\t{har_dir}")  # 将har文件转换为py文件
    except Exception:
        Logger.error(traceback.format_exc())


def har_convert_py(path=''):
    """
    将目录下的所有har文件转换为.py文件
    :return:
    # """
    har_dir = Path.har_path + path

    # 用于存储har文件
    all_file = []

    try:
        # 获取所有文件
        files = get_all_files(har_dir)
        for i in files:
            if i.endswith(".har"):  # 判断.har结尾的文件
                f_name = os.path.join(har_dir, i)  # 将文件和路径合并
                all_file.append(f_name)

        for j in all_file:
            os.system(f"har2case\t{j}")  # 将har文件转换为py文件
    except Exception:
        Logger.error(traceback.format_exc())


def get_test_py(path=''):
    """
    获取test.py文件
    :param path:
    :return:
    """
    global files
    # 存储生成的xxx_test.py文件的路径
    all_file = []

    try:
        # 如果path为空串，获取har目录下的所有.py文件
        if len(path) == 0:
            # 获取目录下的所有文件
            files = get_all_files(Path.har_path)
        else:
            files = get_all_files(path)

        for i in files:
            if i.endswith("test.py"):  # 判断test.py结尾的文件
                all_file.append(i)

        return all_file
    except Exception:
        Logger.error(traceback.format_exc())


def move_py(path=''):
    """
    将.py文件移动到testcases目录
    :return:
    """
    try:
        for i in get_test_py(path):

            # 获取har文件下的文件
            har_file = i.split("har")[1].split(os.sep)  # os.sep    mac根据/切割，如果是win根据\

            # 拼接case目录
            case_path = Path.case_path + os.sep.join(har_file[1:-1])

            if not os.path.exists(case_path):
                # 如果目录不存在，递归创建。适用于多级目录
                os.makedirs(case_path)

            # 用于判断testcase是否已经存在该文件
            case_file = case_path + os.sep + har_file[-1]

            # shutil.move()不会覆盖
            # shutil.copy()会强制覆盖
            # 如果testcase不存在.py文件就移动，如果存在就删除
            if not os.path.exists(case_file):
                shutil.move(i, case_path)
            else:
                if os.path.exists(i):
                    os.remove(i)
                else:
                    Logger.error("文件不存在或已移动")
    except Exception:
        Logger.error(traceback.format_exc())


if __name__ == '__main__':
    har_convert_py_one("test/webportallogin.har")
    # move_py("/Users/cx2259/project/hengshi/api_auto_test/har/test/")
    # a = get_test_py("/har/test")
    # print(a)
