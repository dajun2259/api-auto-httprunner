#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : yaml_py_utils.py
# @Author: 尘心2259
# @Date  : 2023/1/3 15:44
# @Desc  : 将yaml转换为指定模板的py文件
import os
import traceback

from utils.file_utils.case_auto_param import CaseAutoParam
from utils.file_utils.yaml_utils import YamlUtils
from utils.log_utils.loguru_utils import Logger


def write_case(case_path, page):
    """ 写入用例数据 """
    with open(case_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(class_title, data_path, run_request, method, api, case_path, class_title2):
    """

    :param run_request:
    :param run_equest:
    :param class_title:
    :param data_path:
    :param runrequest:
    :param method:
    :param api:
    :param case_path:
    :param class_title2:
    :return:
    """
    page = '''import pytest
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import Parameters
from utils.data_processing.yaml_process import YamlProcess


class %s(HttpRunner):

    @pytest.mark.parametrize('param',
                             Parameters(
                                 YamlProcess().htp_param("%s")))
    def test_start(self, param):
        super().test_start(param)

    config = (
        Config("$configs")
            .variables(**{})
            .base_url("$host")
            .verify(False)
            .export(*[])
    )

    teststeps = [
        Step(
            RunRequest("%s")
                .%s("$host%s")
                .with_params(
                **{}
            )
                .with_headers(
                **{}
            )
                .with_cookies(
                **{}
            )   .with_json({})
                .extract()
                .validate()
                .assert_equal("status_code", "$code")
        ),
    ]


if __name__ == "__main__":
    %s().test_start()
    ''' % (class_title, data_path, run_request, method, api, class_title2)
    try:
        real_time_update_test_cases = YamlUtils().conf_yaml("config.yaml")["real_time_update_test_cases"]

        # False时，已生成的代码不会在做变更
        # 为True的时候，修改yaml文件的用例，代码中的内容会实时更新
        if real_time_update_test_cases:
            write_case(case_path=case_path, page=page)
        elif real_time_update_test_cases is False:
            if not os.path.exists(case_path):
                write_case(case_path=case_path, page=page)
    except Exception:
        Logger().error(traceback.format_exc())


def case_automatic(filepath):
    """
    根据yaml生成case
    :param filepath:
    :return:
    """
    obj = CaseAutoParam(filepath)
    class_title = obj.class_title()
    method_data = obj.yaml_request()
    write_testcase_file(class_title=class_title,
                        data_path=obj.case_data_path(),
                        run_request=obj.run_request(),
                        method=method_data["method"],
                        api=method_data["api"],
                        case_path=obj.case_path(),
                        class_title2=class_title
                        )


if __name__ == '__main__':
    case_automatic("/Users/cx2259/project/api/api_auto_httprunner/data/demo.yaml")
