#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : csv_utils.py
# @Author: 尘心2259
# @Date  : 2022/10/21 11:58
# @Desc  :
import csv
import traceback

from utils.data_processing.data_type import dict_str_conversion
from utils.log.loguru_utils import Logger


class CsvUtils:
    """
    csv工具类
    """

    def read_csv(self, path):
        """
        读取csv文件
        :param path: 文件路径
        :return:
        """
        try:
            with open(path, "r+", encoding="utf-8") as f:
                result = csv.reader(f)
                result_list = []
                for i in result:
                    result_list.append(i)
                return result_list
        except Exception:
            Logger().error(traceback.format_exc())

    def csv_dict(self, path):
        """
        将csv转换为字典
        :param path: 文件路径
        :return:
        """
        try:
            result = self.read_csv(path)

            # 获取csv第一列作为字典的key
            dict_key = result[0]

            # """
            # 方法一
            # """
            # # 用于存储最终的数据
            # all_list = []
            # # 取出值
            # for value in range(1, len(result)):
            #     dict_csv = {}
            #     for item in range(0, len(dict_key)):
            #         dict_csv[dict_key[item]] = result[value][item]
            #     all_list.append(dict_csv)
            # return all_list

            """
            方法二
            """
            all_list2 = [dict(zip(dict_key, item)) for item in result[1:]]
            return all_list2
        except Exception:
            Logger().error(traceback.format_exc())

    def csv_datatype(self, path):
        """
        1.将csv转换为字典
        2.根据约定好的k，将v转换为相应的数据类型
        3.最终将v存储在列表套列表的形式：[[1,2,3],[4,5,6]]
        :param path:
        :return:
        """
        # 存储最终数据
        all_list = []

        try:
            # csv转换字典
            results = self.csv_dict(path)

            for result in results:
                # 转换数据类型
                data = dict_str_conversion(result)

                # 将每次取出的值存储在列表里
                csv_value = []

                # 取出value
                for k, v in data.items():
                    csv_value.append(v)
                all_list.append(csv_value)
            return all_list
        except Exception:
            Logger().error(traceback.format_exc())


if __name__ == '__main__':
    a = CsvUtils().csv_datatype("/Users/cx2259/project/hengshi/api_auto_test/data/data2.csv")
    print(a)
