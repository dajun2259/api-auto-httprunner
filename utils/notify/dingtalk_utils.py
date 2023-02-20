#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dingtalk_utils.py
# @Author: 尘心2259
# @Date  : 2022/6/9 22:52
# @Desc  :
import base64
import hashlib
import hmac
import time
import traceback
import urllib.parse
from typing import Any

from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink

from common.setting import Path
from utils.allure_utils.allure_report_data import CaseCount
from utils.file_utils.yaml_utils import YamlUtils
from utils.loguru_utils import Logger


class DingTalkSendMsg:
    """
        pass
    """

    def __init__(self):

        # 获取config数据
        self.config_data = YamlUtils().read_yaml(Path.config_path + "config.yaml")

        self.timeStamp = str(round(time.time() * 1000))
        self.sign = self.get_sign()

        # 从yaml文件中获取钉钉配置信息
        self.getDingTalk = self.config_data['ding_talk']
        self.project_name = self.config_data['project_name']
        self.tester_name = self.config_data['tester_name']

        # 获取 webhook地址
        self.webhook = self.getDingTalk["webhook"] + "&timestamp=" + self.timeStamp + "&sign=" + self.sign
        self.xiaoDing = DingtalkChatbot(self.webhook)
        self.Process = CaseCount()

    def get_sign(self) -> str:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        try:
            secret = self.config_data['ding_talk']['secret']
            string_to_sign = '{}\n{}'.format(self.timeStamp, secret).encode('utf-8')
            hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
            sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
            return sign
        except Exception:
            Logger.error(traceback.format_exc())

    def send_text(self, msg: str, mobiles=None) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        try:
            if not mobiles:
                self.xiaoDing.send_text(msg=msg, is_at_all=True)
            else:
                if isinstance(mobiles, list):
                    self.xiaoDing.send_text(msg=msg, at_mobiles=mobiles)
                else:
                    raise TypeError("mobiles类型错误 不是list类型.")
        except Exception:
            Logger.error(traceback.format_exc())

    def send_link(self, title: str, text: str, message_url: str, pic_url: str) -> None:
        """
        发送link通知
        :return:
        """
        try:
            self.xiaoDing.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)
        except Exception:
            Logger.error(traceback.format_exc())
            raise

    def send_markdown(self, title: str, msg: str, mobiles=None, is_at_all=False) -> None:
        """

        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """
        try:
            if mobiles is None:
                self.xiaoDing.send_markdown(title=title, text=msg, is_at_all=is_at_all)
            else:
                if isinstance(mobiles, list):
                    self.xiaoDing.send_markdown(title=title, text=msg, at_mobiles=mobiles)
                else:
                    raise TypeError("mobiles类型错误 不是list类型.")
        except Exception:
            Logger.error(traceback.format_exc())

    @staticmethod
    def feed_link(title: str, message_url: str, pic_url: str) -> Any:
        """

        :param title:
        :param message_url:
        :param pic_url:
        :return:
        """
        try:
            return FeedLink(title=title, message_url=message_url, pic_url=pic_url)
        except Exception:
            Logger.error(traceback.format_exc())

    def send_feed_link(self, *arg) -> None:
        """

        :param arg:
        :return:
        """
        try:
            self.xiaoDing.send_feed_card(list(arg))
        except Exception:
            Logger.error(traceback.format_exc())
            raise

    def send_ding_notification(self):
        """

        :return:
        """
        try:
            # 发送钉钉通知
            text = f"#### {self.project_name}自动化通知\n\n" \
                   f">Python脚本任务: {self.project_name}\n\n" \
                   f">环境: TEST\n\n>" \
                   f"执行人: {self.tester_name}\n\n" \
                   f">用例成功率: {self.Process.pass_rate()}%\n\n" \
                   f">总用例数: {self.Process.total_count()}\n\n" \
                   f">成功用例数: {self.Process.pass_count()}\n\n" \
                   f">失败用例数: {self.Process.failed_count()}\n\n" \
                   f">异常用例数: {self.Process.broken_count()}\n\n" \
                   f">跳过用例数: {self.Process.skipped_count()}\n\n" \
                   f" ![screenshot](http://www.1stcs.net/img/homebanner.jpg)\n"
            DingTalkSendMsg().send_markdown(
                title="【自动化通知】",
                msg=text
            )
        except Exception:
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    DingTalkSendMsg().send_ding_notification()
