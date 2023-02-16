# NOTE: Generated By HttpRunner v3.1.6
# FROM: har/itil/event_management/event_list/creat_event.har

import pytest
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import Parameters

from common.setting import *
from utils.file_utils.yaml_utils import YamlUtils

curPath = os.path.abspath(os.path.dirname(__file__))


class TestCaseAddEvent(HttpRunner):

    @pytest.mark.parametrize("param",
                             Parameters(YamlUtils().htp_param("itil/event_management/event_list/add_event.yaml", 1)))
    def test_start(self, param):
        super().test_start(param)

    config = Config("$configs") \
        .base_url("$baseurl") \
        .export(*["ids"]) \
        .verify(False)

    teststeps = [
        Step(
            RunRequest("创建事件")
            .setup_hook('${setup_hooks_request($request)}')
            .post("$baseurl/webportal/itil/command/incident/add")
            .with_params()
            .with_headers(
                **{
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "x-appkey": "20aT2LDaBDmWG12b",
                    "x-tz": "-8",
                    "x-tid": "10",
                    "authorization": "34add2a6503a7dbe1d789b57a4172484",
                    "tenantid": "10",
                    "x-lang": "zh",
                    "accept": "application/json, text/plain, */*",
                    "x-user-token": "34add2a6503a7dbe1d789b57a4172484",
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                    "tenanttype": "1",
                    "sec-ch-ua-platform": '"macOS"',
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "$baseurl/console/index.html",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "projectId": "",
                    "projectName": "",
                    "Admin-Token": "34add2a6503a7dbe1d789b57a4172484",
                    "SERVERID": "983d2c9a307ccc09a34d86554aac4912|1661410939|1661400368",
                }
            )
            .with_json("$data")
            .extract()
            .with_jmespath("body.result.id", "ids")  # 新增事件后返回事件id，用于其他接口调用
            .validate()
            .assert_equal("status_code", "$code")
            .assert_equal("body.ecode", 0)
            .assert_equal("body.reason", "$reason")
        )
    ]


if __name__ == '__main__':
    TestCaseAddEvent().test_start()
