#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project : api_auto_httprunner
# @File    : login.py
# @Time    : 2023-02-21 17:10:12
# @User    : cx2259
# @Author  : 大君
# @Description :
import json
from pprint import pprint

import requests


def login():
    url = "https://www.wanandroid.com/user/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    data = {
        "username": "大君2259",
        "password": 123456

    }
    r = requests.post(url=url, headers=headers, data=data, verify=False)
    response_cookie = r.cookies
    cookies = ''
    for k, v in response_cookie.items():
        _cookie = k + "=" + v + ";"
        # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
        cookies += _cookie
    return cookies


def add_site():
    url = "https://www.wanandroid.com/lg/collect/addtool/json"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": login()
    }
    data = {
        "name": "大君",
        "link": "大君"
    }
    r = requests.post(url=url, headers=headers, data=data, verify=False)
    return r.json()


if __name__ == '__main__':
    a = add_site()
    print(a)
