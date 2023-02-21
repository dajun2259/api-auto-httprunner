import time
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


if __name__ == '__main__':
    pass
