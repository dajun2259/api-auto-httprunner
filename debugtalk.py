import time
from pprint import pprint

import requests
from httprunner import __version__

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils

config = YamlUtils().read_yaml(Path.config_path + "config.yaml")


def get_httprunner_version():
    """

    :return:
    """
    return __version__


def sum_two(m, n):
    """

    :param m:
    :param n:
    :return:
    """

    return m + n


def sleep(n_secs):
    """

    :param n_secs:
    :return:
    """
    time.sleep(n_secs)


def timestamps():
    """
    自动获取时间戳
    :return:
    """
    return int(round(time.time() * 1000))


def login():
    url = "https://www.wanandroid.com/user/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    data = {
        "username": 18800000001,
        "password": 123456

    }
    r = requests.post(url=url, headers=headers, data=data,verify=False)
    return r.headers


if __name__ == '__main__':
    a = login()
    pprint(a)
