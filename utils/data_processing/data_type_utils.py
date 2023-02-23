#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : data_type_utils.py
# @Author: 尘心2259
# @Date  : 2022/10/22 00:50
# @Desc  :
import traceback
from typing import *
import yaml
import json

from common.setting import Path
from utils.log_utils.loguru_utils import Logger

common_path = Path.common_path


def str_conversion(data: Dict) -> dict:
    """
    这是根据字段名判断，然后转换值的数据类型
    :param data:
    :return:
    """
    datatype = ['str', 'Str', 'STR',
                'int', 'Int', 'INT',
                'float', 'Float', 'FLOAT',
                'bool', 'Bool', 'BOOL',
                'none']

    try:
        if isinstance(data, dict):
            for k, v in data.items():

                # 转换为小写
                x_k = k.lower()

                if x_k.__contains__("str"):
                    if len(v) != 0:
                        data[k] = str(v)
                    else:
                        data[k] = ''
                elif x_k.__contains__("int"):

                    if len(v) != 0:
                        data[k] = int(v)
                    else:
                        data[k] = ''
                elif x_k.__contains__("float"):
                    if len(v) != 0:
                        data[k] = float(v)
                    else:
                        data[k] = ''
                elif x_k.__contains__("bool"):
                    if len(v) != 0:
                        data[k] = bool(v)
                    else:
                        data[k] = ''
                elif x_k.__contains__("none"):
                    data[k] = None
                else:
                    print(f"未包含{datatype}关键字")
        else:
            print("数据类型必须是字典")

        return data

    except Exception as e:
        Logger.error(traceback.format_exc())


def dict_str_conversion(data: Dict) -> dict:
    """

    :param data: 值默认是str格式
    :return:
    """
    try:
        if isinstance(data, dict):
            for k, v in data.items():
                if len(v) != 0:
                    if v.endswith('int'):
                        data[k] = int(v.split('-')[0])
                    elif v.endswith('float'):
                        data[k] = float(v.split('-')[0])
                    elif v.endswith('bool'):
                        data[k] = bool(v.split('-')[0])
                    elif v.endswith('none'):
                        data[k] = None

                # 长度为0转换为空字符串
                else:
                    data[k] = ''

        return data

    except Exception as e:
        Logger.error(traceback.format_exc())


def list_deduplication(data: list):
    """

    :param data:
    :return:
    """
    # 存储去重后的数据
    result_data = []
    try:
        if isinstance(data, list):
            for i in data:
                if i not in result_data:
                    result_data.append(i)
        return result_data
    except Exception:
        Logger.error(traceback.format_exc())


def json_to_yaml(i):
    """
    json转为yaml
    :param i: 读取的文件
    :return:
    """
    with open(common_path + i, encoding="utf-8") as f:
        datas = json.load(f)  # 将文件的内容转换为字典形式
    yaml_datas = yaml.dump(datas, indent=5, sort_keys=False, Dumper=yaml.SafeDumper, allow_unicode=True,
                           default_flow_style=False)  # 将字典的内容转换为yaml格式的字符串
    print(yaml_datas)


def yaml_to_json(i):
    """
    yaml转为json,存入文件
    :param i:
    :return:
    """

    with open(common_path + i, "r", encoding="utf-8") as f:
        datas = yaml.load(f, Loader=yaml.SafeLoader)  # 将文件的内容转换为字典形式
    json_datas = json.dumps(datas, indent=5, ensure_ascii=False)  # 将字典的内容转换为json格式的字符串
    print(json_datas)


if __name__ == '__main__':
    json_to_yaml("yaml_json/i")
