#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : import_har.py
# @Author: 尘心2259
# @Date  : 2022/11/15 15:35
# @Desc  : 该工具是将har文件导入到ms平台
import json
import time

import requests

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils

ms_info = YamlUtils().read_yaml(Path.config_path + "ms.yaml")


class ImportHar:
    """
    将har文件导入到ms平台
    """

    def __init__(self):
        # 协议
        self.p = "https"
        # ip、端口
        self.ip_port = ms_info["ms"]["ip_port"]
        # 公用请求信息
        self.contenttype = "application/json"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
        # 工作空间
        self.workspace_id = ms_info["ms"]["workspace_id"]  # 这是默认工作空间id，一般不变
        # 项目id
        self.project_id = ms_info["ms"]["project_id"]  # 这是项目id，每个项目id不一样

    def ms_login(self):
        """

        :param user: 账户
        :param pwd: 密码
        :return:
        """
        url = f"{self.p}://{self.ip_port}/ldap/signin"

        herder = {
            "Content-Type": self.contenttype,
            "User-Agent": self.user_agent
        }
        payload = {
            "username": ms_info["ms"]["user"],
            "password": ms_info["ms"]["pwd"],
            "authenticate": "LOCAL"
        }

        r = requests.post(url=url, json=payload, headers=herder, verify=False)

        return {
            "sessionId": r.json()["data"]["sessionId"],
            "csrfToken": r.json()["data"]["csrfToken"]
        }

    def metersphere_definition_import_har(self, harname, payload):
        """
        这个方法是在metersphere的接口定义模块中导入har文件
        :param harname:
        :param payload:
        :return:
        """

        # 模块id
        module_id = ms_info["ms"]["definition"]["module_id"]  # 模块id。每个项目下面有多个模块
        # 模块名称
        module_path = ms_info["ms"]["definition"]["module_path"]  # 模块名称

        # 获取token
        login_info = self.ms_login()

        # 获取13位时间戳
        timestamp = int(round(time.time() * 1000))

        url = f"{self.p}://{self.ip_port}/api/api/definition/import"

        # 如需headers，不需要赋值Content-Type,不然会报错
        herder = {
            # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryZFLQt0yHH5I9m3HU",
            "PROJECT": self.project_id,
            "WORKSPACE": self.workspace_id,
            "CSRF-TOKEN": login_info["csrfToken"],
            "X-AUTH-TOKEN": login_info["sessionId"]
        }

        text = {"file": {"uid": timestamp}, "modeId": "incrementalMerge",
                "moduleId": module_id, "modulePath": module_path, "platform": "Har",
                "saved": True, "model": "definition", "projectId": self.project_id,
                "protocol": "HTTP"}

        m = {"file": (harname, json.dumps(payload), 'application/octet-stream'),

             "request": ('blob', json.dumps(text), 'application/json')

             }

        r = requests.post(url=url, files=m, headers=herder, verify=False)
        return r.json()

    def metersphere_automation_import_har(self, harname, payload):
        """
        这个方法是在metersphere的接口自动化模块中导入har文件
        :param harname:
        :param payload:
        :return:
        """

        # 模块id
        module_id = ms_info["ms"]["automation"]["module_id"]  # 模块id。每个项目下面有多个模块
        # 模块名称
        module_path = ms_info["ms"]["automation"]["module_path"]  # 模块名称

        # 获取token
        login_info = self.ms_login()

        # 获取13位时间戳
        timestamp = int(round(time.time() * 1000))

        url = f"{self.p}://{self.ip_port}/api/api/automation/import"

        # 如需headers，不需要赋值Content-Type,不然会报错
        herder = {
            # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryZFLQt0yHH5I9m3HU",
            "PROJECT": self.project_id,
            "WORKSPACE": self.workspace_id,
            "CSRF-TOKEN": login_info["csrfToken"],
            "X-AUTH-TOKEN": login_info["sessionId"]
        }

        text = {"file": {"uid": timestamp}, "modeId": "incrementalMerge",
                "moduleId": module_id, "coverModule": False, "modulePath": module_path,
                "platform": "Har", "saved": True, "projectId": self.project_id}

        m = {"file": (harname, json.dumps(payload), 'application/octet-stream'),

             "request": ('blob', json.dumps(text), 'application/json')

             }

        r = requests.post(url=url, files=m, headers=herder, verify=False)
        return r.json()


if __name__ == '__main__':
    pass
