#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : run.py.py
# @Author: 尘心2259
# @Date  : 2022/7/13 19:41
# @Desc  :
import os

import pytest

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils
from utils.loguru_utils import Logger

config = YamlUtils().read_yaml(Path.config_path + "config.yaml")


def run(case_dir):
    """

    :param case_dir: testcases里的用例目录
    :return:
    """
    case_path = Path.case_path + case_dir

    Logger().info(

        """
           _    _         _      _____         _
          / \\  _   _| |_ __|_   _|__  ___| |_
         / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
        / ___ \\ |_| | || (_) | |  __/\\__ \\ |_
       /_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|

        """
    )

    pytest.main([f'{case_path}',
                 '-s',
                 '-n=2',
                 '--alluredir', './report/tmp', "--clean-alluredir"
                 ]
                )

    os.system(r"allure generate ./report/tmp -o ./report/html --clean")
    # os.system(f"allure serve ./report/tmp  -p 811") # 执行完自动打开报告，指定固定端口

    # 发送钉钉通知
    # DingTalkSendMsg().send_ding_notification()


if __name__ == '__main__':
    run("itil/event_management/event_list/query_event_test.py")
