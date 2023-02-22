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

from common.setting import Path
from utils.file_utils.files_utils import get_all_files
from utils.file_utils.yaml_utils import YamlUtils
from utils.loguru_utils import Logger

config_result = YamlUtils().read_yaml(Path.common_path + "config.yaml")


class UpdateData:
    def __init__(self):
        self.curPath = Path.root_path + "utils/update_utils/"
        self.jiancha = "config = ("
        self.urls = config_result['host']
        self.hosts = "$Host"
        self.base_url = "$BASE_URL"

    def read(self, file_name):
        with open(self.curPath + file_name, 'r', encoding='utf-8') as f:
            return f.read()

    def Test_Data(self):
        """
        该替换只适用于录制接口
        :return:
        """
        global url_a, Runrequest, NewRunrequest, Hook, data, Data_Hook, Data_URL, ConFig, data_Host, Data_Import, replace_validate

        hooks = self.read('替换的hook')
        tihuan = self.read('替换的列表')
        tihuan_Import = self.read('UP_tou')
        new_validate = self.read('替换validate')

        case_path = Path.case_path + config_result['updata_path']
        path_dir = get_all_files(case_path)

        for all_dir in path_dir:
            if all_dir.endswith("_test.py"):
                sub_dir = os.path.join(case_path, all_dir)
                '''1开始添加Hook到文件中'''
                try:
                    with open(sub_dir, 'r', encoding='utf-8') as f:
                        data = f.read()
                    # 查找第二个Runrequest内的信息
                    Runrequest = re.findall('RunRequest(.+)', data)[1]
                except Exception:
                    pass
                try:
                    # 开始添加setup_hook
                    Hook = re.findall('setup_hook(.+)', data)[0]
                    Data_Hook = data
                except Exception:
                    NewRunrequest = Runrequest + hooks
                    Data_Hook = data.replace(Runrequest, NewRunrequest)


                '''2把文件内的所有请求地址更换成$BASE_URL变量地址'''
                try:
                    test_interface_path = re.findall(self.urls, Data_Hook)[0]
                    # 开始替换请求地址为变量
                    if "Parameters" not in Data_Hook: # Parameters不在的话在替换，否则就会将原先域名替换成"$BASE_URL"，会跟豪哥的不一样。
                        if test_interface_path == self.urls:
                            Data_URL = Data_Hook.replace(test_interface_path, self.base_url)
                    else:
                        Data_URL = Data_Hook
                except Exception:
                    Data_URL = Data_Hook

                '''3把文件内所有config替换一下'''
                try:
                    configb = re.findall('config.*.', Data_URL)[0]
                    if configb != self.jiancha:
                        ConFig = Data_URL.replace(configb, tihuan)
                    else:
                        ConFig = Data_URL
                except Exception:
                    ConFig = Data_URL
                '''4把所有的host更换成env变量'''
                try:
                    hosta = re.findall('"Host": "(.+)"', ConFig)[0]
                    # 开始替换hosts
                    if hosta != self.hosts:
                        data_Host = ConFig.replace(hosta, self.hosts)
                    else:
                        data_Host = ConFig
                    # with open(sub_dir, 'w', encoding='utf-8') as w:
                    #     w.write(data_Host)
                except Exception:
                    data_Host = ConFig

                '''修改导入的库'''
                try:
                    runner = re.findall(".*HttpRunner,.*", data_Host)[0]
                    # 开始替换头文件
                    if tihuan_Import in data_Host:
                        Data_Import = data_Host
                    else:
                        Data_Import = data_Host.replace(runner, tihuan_Import)
                except Exception as e:
                    pass

                ''' 替换validate()'''
                try:
                    validate = re.findall('(\.validate\(\))', Data_Import)[0]
                    if new_validate in Data_Import:
                        replace_validate = Data_Import

                    elif ".extract()" in Data_Import:
                        replace_validate = Data_Import

                    elif ".validate()" in Data_Import:
                        replace_validate = Data_Import.replace(validate, new_validate)

                    else:
                        replace_validate = Data_Import.replace(validate, new_validate)

                except Exception:
                    pass

                '''把上面修改好的数据替换到换文件内'''
                try:
                    with open(sub_dir, 'w', encoding='utf-8') as w:
                        w.write(replace_validate)
                except Exception:
                    pass

            else:
                if all_dir.endswith(".py"):
                    Logger.warning(f"{all_dir}不是_test.py结尾，不能修改信息")



if __name__ == '__main__':
    UpdateData().Test_Data()

