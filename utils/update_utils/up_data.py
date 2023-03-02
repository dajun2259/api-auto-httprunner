# !/usr/bin/env/ python3
# -*- coding:utf-8 -*-
import os
import os.path
import re
import traceback

from common.setting import Path
from utils.file_utils.files_utils import *
from utils.file_utils.yaml_utils import YamlUtils
from utils.log_utils.loguru_utils import Logger

config_result = YamlUtils().read_yaml(Path.common_path + "config.yaml")


class UpData:
    def __init__(self):
        self.cur_path = Path.root_path + "utils/update_utils/"
        self.urls = config_result['host']
        self.base_url = "$baseurl"

    def read(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            Logger().error(traceback.format_exc())

    def write(self, file_name, content):
        try:
            with open(file_name, 'w', encoding='utf-8') as w:
                w.write(content)
        except Exception:
            Logger().error(traceback.format_exc())

    def up_htp_data(self):
        """
        该替换只适用于录制接口
        :return:
        """
        try:
            new_hook = self.read(self.cur_path + 'up_hook')
            new_up = self.read(self.cur_path + 'up_setup')
            new_head = self.read(self.cur_path + 'up_head')
            new_validate = self.read(self.cur_path + 'up_validate')

            case_path = Path.case_path + config_result['update_path']
            path_dir = get_test_py_path(case_path)

            for all_dir in path_dir:
                # 读取文件内容
                read_content = self.read(all_dir)

                # 修改导入的库
                get_httprunner = re.findall(".*HttpRunner,.*", read_content)[0]
                if new_head in read_content:
                    data_import = read_content
                else:
                    data_import = read_content.replace(get_httprunner, new_head)

                # 修改config
                get_config = re.findall('config.*.', data_import)[0]
                if new_up in read_content:
                    data_config = read_content
                else:
                    data_config = data_import.replace(get_config, new_up)

                # 添加hook
                get_runrequest = re.findall('RunRequest(.+)', data_config)[0]
                if new_hook in read_content:
                    data_hook = read_content
                else:
                    data_hook = data_config.replace(get_runrequest, get_runrequest + new_hook)

                # 替换baseurl
                get_urls = re.findall(self.urls, data_hook)[0]
                if self.base_url in read_content:
                    data_url = read_content
                else:
                    data_url = data_hook.replace(get_urls, self.base_url)

                # 替换validate()
                get_validate = re.findall('(\.validate\(\))', data_import)[0]
                if new_validate in read_content:
                    data_validate = read_content

                else:
                    data_validate = data_url.replace(get_validate, new_validate)

                # 将最终的内容重新写入文件
                self.write(all_dir, data_validate)
                # print(data_validate)

        except Exception:
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    UpData().up_htp_data()
