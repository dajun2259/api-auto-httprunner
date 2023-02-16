#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : case_auto_param.py
# @Author: 尘心2259
# @Date  : 2023/1/4 10:04
# @Desc  :
import os
import traceback

from common.setting import Path
from utils.file_utils.files_utils import file_capitalize, creat_path, creat_init_py
from utils.file_utils.yaml_utils import YamlUtils
from utils.loguru_utils import Logger


class CaseAutoParam:
    """
        生成自动化case模板的所需要的参数
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = YamlUtils().read_yaml(self.filepath)

    def class_title(self):
        """
        用于类名

        :return:
        """
        try:
            if self.filepath.endswith(".yaml") or self.filepath.endswith("yml"):
                return "TestCase"+file_capitalize(self.filepath)
        except Exception:
            Logger().error(traceback.format_exc())

    def case_data_path(self):
        """
        获取data目录下的yaml路径
        :return:
        """
        try:
            data_path = self.filepath.split(f"data{os.sep}")[1]  # macs上os.sep代表/，win代表\\
            return data_path
        except Exception:
            Logger().error(traceback.format_exc())

    def case_path(self):
        """
        拼接case存储路径
        :return:
        """

        try:
            split_data_path = self.case_data_path().split(f"{os.sep}")
            path = f'{os.sep}'.join(split_data_path[:-1]) + os.sep
            new_case_path = Path.case_path + path
            # 目录不存在则创建
            creat_path(new_case_path)
            # 如果目录下不存在__init__.py文件，则创建
            creat_init_py(new_case_path)

            # case_name
            yaml_name = split_data_path[-1]
            case_name = None
            if yaml_name.endswith(".yaml"):
                case_name = yaml_name.split(".yaml")[0] + "_test.py"
            elif yaml_name.endswith(".yml"):
                case_name = yaml_name.split(".yml")[0] + "_test.py"

            return new_case_path + case_name
        except Exception:
            Logger().error(traceback.format_exc())

    def yaml_request(self):
        """

        :return:
        """
        try:
            # 存储最终数据
            data_dict = {}
            # 提取指定keys的数据,不支持值是字典、列表格式的
            request_keys = ["method", "api"]
            for k, v in self.data.items():
                for k2 in request_keys:
                    if k2 in v:
                        data_dict[k2] = v[k2]
            # 将值转换为小写
            data_dict["method"].lower()
            return data_dict
        except Exception:
            Logger().error(traceback.format_exc())

    def case_common(self):
        """
        返回yaml中公共参数
        :return:
        """
        try:
            common_dict = {}
            for k, v in self.data["case_common"].items():
                common_dict[k] = v
            return common_dict
        except Exception:
            Logger().error(traceback.format_exc())

    def run_request(self):
        """
        :return:
        """
        v_list = []
        for k, v in self.case_common().items():
            v_list.append(v)
        return '-'.join(v_list)


if __name__ == '__main__':
    a = CaseAutoParam("/Users/cx2259/project/hengshi/api_auto_test/data/itil/test/query_event.yaml").class_title()
    print(a)
