import traceback
from pprint import pprint

import yaml

from common.setting import Path
from utils.data_type_utils import list_deduplication
from utils.loguru_utils import Logger


class YamlUtils:
    """
        yaml方法
    """

    def __init__(self):
        self.root_path = Path()
        self.common_path = self.root_path.common_path
        self.data_path = self.root_path.data_path

    def read_yaml(self, filename):
        """

        :param filename:
        :return:
        """
        try:
            with open(filename, "r", encoding="utf8") as f:
                result = yaml.load(f, Loader=yaml.SafeLoader)
                return result
        except Exception as e:
            Logger().error(traceback.format_exc())

    def write_yaml(self, filename, data):
        """

        :param filename:
        :param data:
        :return:
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump(data, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False)
        except Exception:
            Logger().error(traceback.format_exc())

    def conf_yaml(self, filename):
        """

        :param filename:
        :return:
        """
        try:
            return self.read_yaml(self.conf_path + filename)
        except Exception:
            Logger().error(traceback.format_exc())

    def htp_param(self, filename, tag=None):
        """
        根据httprunner发送请求要求，做出的数据清洗
        :param tag: 如果data想发送一个大json数据，随便给tag一个值就行
        :param filename:
        :return:
        """
        results = self.read_yaml(self.data_path + filename)
        # 存储最终value
        all_list = []

        # 存储所有key
        all_key = []

        # 值不是字段的key
        conf_key = ["configs", "case_name", "baseurl", "host", "sql"]

        try:
            # 删除case_common，这里不需要
            results.pop("case_common")

            for result in results.items():
                value = []
                # 将值不是字典的数据先添加
                for k, v in result[1].items():
                    if k in conf_key:
                        all_key.append(str(k))
                        value.append(v)
                if tag is None:
                    # 获取data数据
                    for data_k, data_v in result[1]["data"].items():
                        all_key.append(str(data_k))
                        value.append(data_v)
                else:
                    all_key.append("data")
                    value.append(result[1]["data"])

                # 获取assert数据
                for assert_k, assert_v in result[1]["assert"].items():
                    all_key.append(str(assert_k))
                    value.append(assert_v)

                all_list.append(value)

            # -符号拼接key,并对key去重
            join_key = "-".join(list_deduplication(all_key))

            # 返回以下json格式
            """
                {
                    'a-b':[[1,2],[3,4]]
                }
            """

            return {
                join_key: all_list
            }

        except Exception as e:
            Logger().error(traceback.format_exc())


if __name__ == '__main__':
    a = YamlUtils().htp_param(
        "collect/collect_add_site.yaml")
    pprint(a)
