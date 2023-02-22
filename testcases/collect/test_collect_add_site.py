import pytest
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import Parameters
from utils.file_utils.yaml_utils import YamlUtils


class TestCaseCollectAddSite(HttpRunner):

    @pytest.mark.parametrize('param',
                             Parameters(
                                 YamlUtils().htp_param("collect/collect_add_site.yaml")))
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
            RunRequest("开发平台-收藏模块-添加网站")
            .post("$host/lg/collect/addtool/json")
            .with_params(
                **{}
            )
            .with_headers(
                **{
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "Cookie": "${login_init()}"
                }
            )
            .with_cookies(
                **{
                }
            ).with_data({
                "name": "$name",
                "link": "$link"
            })
            .extract()
            .validate()
            .assert_equal("status_code", "$code")
            .assert_equal("body.data.name", "$msg")
        ),
    ]


if __name__ == "__main__":
    TestCaseCollectAddSite().test_start()
