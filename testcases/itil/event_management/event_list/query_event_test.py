import pytest
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import Parameters
from utils.file_utils.yaml_utils import YamlUtils


class TestCaseQueryEvent(HttpRunner):

    @pytest.mark.parametrize('param',
                             Parameters(
                                 YamlUtils().htp_param("itil/event_management/event_list/query_event.yaml")))
    def test_start(self, param):
        super().test_start(param)

    config = (
        Config("$configs" + "—" + "$case_name")
        .variables(**{})
        .base_url("$baseurl")
        .verify(False)
        .export(*[])
    )

    teststeps = [
        Step(
            RunRequest("事件管理-事件列表-查询事件")

            .setup_hook('${setup_hooks_request($request)}')
            .get("$baseurl/webportal/itil/query/incidents")
            .with_params(
                **{
                    "page": "1",
                    "limit": "30",
                    "needTotal": "true",
                    "includes": "WITH_FILE,WITH_REF,WITH_CREATER,WITH_TASK,WITH_SCI,WITH_EXTFIELD",
                    "skey": "$skey",
                }
            )
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
                }
            )
            .validate()
            .assert_equal("status_code", "$code")
            .assert_equal("body.reason", "$reason")
            .assert_equal("body.result.lists[0].code", "$msg")
        ),
    ]


if __name__ == "__main__":
    TestCaseQueryEvent().test_start()
