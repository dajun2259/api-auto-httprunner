#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/29 14:57
# @Author : 尘心

import smtplib
import traceback
from email.mime.text import MIMEText

from common.setting import Path
from utils.allure_utils.allure_report_data import CaseCount, AllureFileClean
from utils.file_utils.yaml_utils import YamlUtils
from utils.log_utils.loguru_utils import Logger


class SendEmail:
    def __init__(self):

        self.config_data = YamlUtils().read_yaml(Path.common_path + "config.yaml")
        self.getData = self.config_data['email']
        self.send_user = self.getData['send_user']  # 发件人
        self.email_host = self.getData['email_host']  # QQ 邮件 STAMP 服务器地址
        self.key = self.getData['stamp_key']  # STAMP 授权码
        self.name = self.config_data['project_name'][0]
        self.allureData = CaseCount()
        self.PASS = self.allureData.pass_count()
        self.FAILED = self.allureData.failed_count()
        self.BROKEN = self.allureData.broken_count()
        self.SKIP = self.allureData.skipped_count()
        self.TOTAL = self.allureData.total_count()
        self.RATE = self.allureData.pass_rate()
        self.CaseDetail = AllureFileClean().get_failed_cases_detail()

    def send_mail(self, user_list: list, sub, content: str) -> None:
        """

        @param user_list: 发件人邮箱
        @param sub:
        @param content: 发送内容
        @return:
        """
        try:
            user = "陈鑫" + "<" + self.send_user + ">"
            message = MIMEText(content, _subtype='plain', _charset='utf-8')
            message['Subject'] = sub
            message['From'] = user
            message['To'] = ";".join(user_list)
            server = smtplib.SMTP()
            server.connect(self.email_host)
            server.login(self.send_user, self.key)
            server.sendmail(user, user_list, message.as_string())
            server.close()
        except Exception:
            Logger.error(traceback.format_exc())

    def error_mail(self, error_message: str) -> None:
        """
        执行异常邮件通知
        @param error_message: 报错信息
        @return:
        """
        try:
            email = self.getData['send_list']
            user_list = email.split(',')  # 多个邮箱发送，config文件中直接添加  '806029174@qq.com'

            sub = self.name + "自动化执行异常通知"
            content = "自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下：\n{0}".format(error_message)
            self.send_mail(user_list, sub, content)
        except Exception:
            Logger.error(traceback.format_exc())

    def send_main(self) -> None:
        """
        发送邮件
        :return:
        """
        try:
            email = self.getData["send_list"]
            user_list = email.split(',')  # 多个邮箱发送，yaml文件中直接添加  '806029174@qq.com'

            sub = self.name + "自动化报告"
            content = """
            各位同事, 大家好:
                自动化用例执行完成，执行结果如下:
                用例运行总数: {} 个
                通过用例个数: {} 个
                失败用例个数: {} 个
                异常用例个数: {} 个
                跳过用例个数: {} 个
                成  功   率: {} %
    
            {}
            """.format(self.TOTAL, self.PASS, self.FAILED, self.BROKEN, self.SKIP, self.RATE, self.CaseDetail)

            self.send_mail(user_list, sub, content)
        except Exception:
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    SendEmail().send_main()
