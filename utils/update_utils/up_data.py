# !/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTest
@File  :APP_copy.py
@Author:alvin.guoxu
@Date  :2021/5/26 18:22
@Desc  : 异步生成脚本
"""
import os
import os.path
import re
import traceback

from common.setting import Path
from utils.file_utils.files_utils import *
from utils.file_utils.yaml_utils import YamlUtils
from utils.log_utils.loguru_utils import Logger

config_result = YamlUtils().read_yaml(Path.common_path + "config.yaml")


class UpdateData:
    def __init__(self):
        self.cur_path = Path.root_path + "utils/update_utils/"
        self.conf = "config = ("
        self.urls = config_result['host']
        self.hosts = "$Host"
        self.base_url = "$baseurl"

    def read(self, file_name):
        with open(self.cur_path + file_name, 'r', encoding='utf-8') as f:
            return f.read()

    def update_data(self):
        """
        该替换只适用于录制接口
        :return:
        """
        try:
            global runrequest, new_runrequest, hook, data, data_hook, data_url, config, data_host, data_import, replace_validate

            new_hook = self.read('up_hook')
            new_up = self.read('up_setup')
            new_head = self.read('up_head')
            new_validate = self.read('up_validate')

            case_path = Path.case_path + config_result['update_path']
            path_dir = get_all_files(case_path)

            for all_dir in path_dir:
                if all_dir.endswith("_test.py"):
                    sub_dir = os.path.join(case_path, all_dir)
                    '''1开始添加hook到文件中'''
                    try:
                        with open(sub_dir, 'r', encoding='utf-8') as f:
                            data = f.read()
                        # 查找第二个Runrequest内的信息
                        Runrequest = re.findall('RunRequest(.+)', data)[1]
                    except Exception:
                        pass
                    try:
                        # 开始添加setup_hook
                        hook = re.findall('setup_hook(.+)', data)[0]
                        data_hook = data
                    except Exception:
                        new_runrequest = runrequest + new_hook
                        data_hook = data.replace(runrequest, new_runrequest)

                    '''2把文件内的所有请求地址更换成$BASE_URL变量地址'''
                    try:
                        test_interface_path = re.findall(self.urls, data_hook)[0]
                        # 开始替换请求地址为变量
                        if "Parameters" not in data_hook:  # Parameters不在的话在替换，否则就会将原先域名替换成"$BASE_URL"，会跟豪哥的不一样。
                            if test_interface_path == self.urls:
                                data_url = data_hook.replace(test_interface_path, self.base_url)
                        else:
                            data_url = data_hook
                    except Exception:
                        data_url = data_hook

                    '''3把文件内所有config替换一下'''
                    try:
                        conf_content = re.findall('config.*.', data_url)[0]
                        if conf_content != self.conf:
                            config = data_url.replace(conf_content, new_up)
                        else:
                            config = data_url
                    except Exception:
                        config = data_url
                    '''4把所有的host更换成env变量'''
                    try:
                        host_content = re.findall('"Host": "(.+)"', config)[0]
                        # 开始替换hosts
                        if host_content != self.hosts:
                            data_host = config.replace(host_content, self.hosts)
                        else:
                            data_host = config
                        # with open(sub_dir, 'w', encoding='utf-8') as w:
                        #     w.write(data_host)
                    except Exception:
                        data_host = config

                    '''修改导入的库'''
                    try:
                        runner = re.findall(".*HttpRunner,.*", data_host)[0]
                        # 开始替换头文件
                        if new_head in data_host:
                            data_import = data_host
                        else:
                            data_import = data_host.replace(runner, new_head)
                    except Exception as e:
                        pass

                    ''' 替换validate()'''
                    try:
                        validate = re.findall('(\.validate\(\))', data_import)[0]
                        if new_validate in data_import:
                            replace_validate = data_import

                        elif ".extract()" in data_import:
                            replace_validate = data_import

                        elif ".up_validate()" in data_import:
                            replace_validate = data_import.replace(validate, new_validate)

                        else:
                            replace_validate = data_import.replace(validate, new_validate)

                    except Exception:
                        pass

                    '''把上面修改好的数据替换到换文件内'''
                    try:
                        with open(sub_dir, 'w', encoding='utf-8') as w:
                            w.write(replace_validate)
                    except Exception:
                        pass

                else:
                    raise f"{all_dir}不是_test.py结尾，不能修改信息"

        except Exception:
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    UpdateData().update_data()
