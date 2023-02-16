import requests

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils

config = YamlUtils().read_yaml(Path.config_path + "config.yaml")


def web_token(base_url, user, passwd, tenantId):
    """

    :param base_url:
    :param user:
    :param passwd:
    :param tenantId:
    :return:
    """
    url = f"{base_url}/webportal/login"

    headers = {
        "content-length": "128",
        "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        "content-type": "application/json;charset=UTF-8",
        "origin": base_url,
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"{base_url}/vue-console/index.html",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": ''
    }

    body = {
        "account": str(user),
        "password": passwd,
        "renewal": True,
        "tenantId": tenantId,
    }
    r = requests.post(url, headers=headers, json=body, verify=False)
    token = r.json()["result"]["token"]
    appkey = r.json()["result"]["appKey"]
    appsecret = r.json()["result"]["appSecret"]
    return token, appkey, appsecret


if __name__ == "__main__":
    a = web_token("https://test.1stcs.cn", 18031160867, "TlRReE5tUTNZMlEyWldZeE9UVmhNR1kzTmpJeVlUbGpOVFppTlRWbE9EUT0=", 522)
    print(a)
