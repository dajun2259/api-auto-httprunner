# !/usr/bin/env/ python3
# -*- coding:utf-8 -*-
import os
import os.path
import re
import traceback

from common.setting import Path
from utils.file.files_utils import *
from utils.file.yaml_utils import YamlUtils
from utils.log.loguru_utils import Logger

config_result = YamlUtils().read_yaml(Path.common_path + "config.yaml")


class UpData:
    def __init__(self):
        self.cur_path = Path.root_path + "utils/update/"
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

    # 这个方法代码过于冗余，优化后可以参考up_htp_data()方法
    def test(self):
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

    def up_htp_data(self):
        """
        该替换只适用于录制接口
        :return:
        """
        try:
            regex_data = [
                ['.*HttpRunner,.*', self.read(self.cur_path + 'up_head'), 0],  # 修改导入的库
                ['config.*.', self.read(self.cur_path + 'up_setup'), 0],  # 修改config
                ['RunRequest(.+)', self.read(self.cur_path + 'up_hook'), 1],  # 添加hook
                [self.urls, self.base_url, 0],  # 替换baseurl
                ['(\.validate\(\))', self.read(self.cur_path + 'up_validate'), 0]  # 替换validate()

            ]

            case_path = Path.case_path + config_result['update_path']
            path_dir = get_test_py_path(case_path)

            for all_dir in path_dir:
                # 读取文件内容
                read_content = self.read(all_dir)

                '''
                 没有该条件判断会报错。如果文件数据已经更新了一次，再次更新后报错，因为更新后的数据，正则表达式已经匹配不到了。
                 所以加判断条件:  如果self.base_url不存在说明还是旧数据，正则是可以匹配到的
                '''
                if self.base_url not in read_content:
                    for i in regex_data:
                        get_regex_data = re.findall(i[0], read_content)[i[2]]
                        read_content = read_content.replace(get_regex_data, i[1])
                self.write(all_dir, read_content)

        except Exception:
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    UpData().up_htp_data()
