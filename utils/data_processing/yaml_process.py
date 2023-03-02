#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project : webui_auto_python
# @File    : yaml_process.py
# @Time    : 2023-02-23 18:35:17
# @User    : cx2259
# @Author  : 大君
# @Description :
import traceback

from utils.data_processing.data_type import list_deduplication
from utils.file.yaml_utils import YamlUtils
from utils.log.loguru_utils import Logger


class YamlProcess(YamlUtils):
    def __int__(self):
        super().__init__()

    def htp_param(self, filename, tag=None):
        """
        根据httprunner发送请求要求，做出的数据清洗
        :param tag: 如果data想发送一个大json数据，随便给tag一个值就行
        :param filename:
        :return:
        """
        results = self.read_yaml(self.data_path + filename)
        # 存储最终value
        all_list = []

        # 存储所有key
        all_key = []

        # 值不是字段的key
        conf_key = ["configs", "case_name", "baseurl", "host", "sql"]

        try:
            # 删除case_common，这里不需要
            results.pop("case_common")

            for result in results.items():
                value = []
                # 将值不是字典的数据先添加
                for k, v in result[1].items():
                    if k in conf_key:
                        all_key.append(str(k))
                        value.append(v)
                if tag is None:
                    # 获取data数据
                    for data_k, data_v in result[1]["data"].items():
                        all_key.append(str(data_k))
                        value.append(data_v)
                else:
                    all_key.append("data")
                    value.append(result[1]["data"])

                # 获取assert数据
                for assert_k, assert_v in result[1]["assert"].items():
                    all_key.append(str(assert_k))
                    value.append(assert_v)

                all_list.append(value)

            # -符号拼接key,并对key去重
            join_key = "-".join(list_deduplication(all_key))

            # 返回以下json格式
            """
                {
                    'a-b':[[1,2],[3,4]]
                }
            """

            return {
                join_key: all_list
            }

        except Exception as e:
            Logger().error(traceback.format_exc())


if __name__ == '__main__':
    a = YamlProcess().htp_param(
        "collect/collect_add_site.yaml")
    print(a)
