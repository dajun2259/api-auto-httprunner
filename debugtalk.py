import time
from httprunner import __version__
from common.setting import Path
from utils.file.yaml_utils import YamlUtils
from utils.login import login

config = YamlUtils().read_yaml(Path.common_path + "config.yaml")


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


def login_init():
    return login()


if __name__ == '__main__':
    a = login_init()
    print(a)
