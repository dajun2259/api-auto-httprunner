#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : run.py.py
# @Author: 尘心2259
# @Date  : 2022/7/13 19:41
# @Desc  :
import os
import pytest
from common.setting import Path
from utils.allure.allure_report_data import AllureFileClean
from utils.log.loguru_utils import Logger
from utils.notify.dingtalk import DingTalkSendMsg
from utils.notify.lark import FeiShuTalkChatBot
from utils.notify.send_mail import SendEmail
from utils.notify.wechat_send import WeChatSend
from utils.other.models import NotificationType
from utils import config


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
                 # '-n=2',
                 '--alluredir', './report/tmp', "--clean-alluredir"
                 ]
                )

    os.system(r"allure generate ./report/tmp -o ./report/html --clean")

    allure_data = AllureFileClean().get_case_count()
    notification_mapping = {
        NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
        NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
        NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
        NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
    }

    if config.notification_type != NotificationType.DEFAULT.value:
        notification_mapping.get(config.notification_type)()

    # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
    # os.system(f"allure serve ./report/tmp -h 127.0.0.1 -p 9999")


if __name__ == '__main__':
    run("collect/test_collect_add_site.py")
