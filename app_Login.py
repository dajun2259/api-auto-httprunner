import time
import requests
from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils

config = YamlUtils().read_yaml(Path.config_path + "config.yaml")


def timestamps():
    aa = (int(round(time.time() * 1000)))
    times = str(aa)
    print(times)
    return times


def app_token(base_url, user, passwd, tenantId):
    """

    :param base_url:
    :param user:
    :param passwd:
    :param tenantId:
    :return:
    """
    url = f"{base_url}/m-openapi/v2/user/oauth2/token"
    headers = {
        "content-encoding": "gzip",
        "cache-control": "no-cache",
        "x-timestamp": "1627539860825",
        "user-agent": "you yune fu/2.5.3 (iPhone; iOS 14.6; Scale/3.00)",
        "x-lang": "zh",
        "x-device": "iPhone-iOS-14.6",
        "x-bundle-id": "com.i1stcs.engineer2",
        "content-length": "272",
        "x-secret-type": "none",
        "x-app-version": "2.5.3",
        "x-appkey": "",
        "authorization": "Basic 0e1d53912c4422ca1f01cdf930f2687e",
        "accept-language": "zh-Hans-CN;q=1",
        "x-secret-code": "b515bbe3186cacaa097822783b43d9ac",
        "accept": "*/*",
        "content-type": "application/json;charset-utf-8",
        "accept-encoding": "gzip, deflate",
        "x-tz": "-8",
    }

    body = {
        "account": user,
        "password": passwd,
        "deviceId": "F725995C-A800-4DDA-9DEB-7A6D350284D6",
        "os": "iOS14.60",
        "cId": "596eb5748607b7761fb8e134cb39ace5",
        "tenantId": tenantId,
        "bundleId": "com.i1stcs.engineer2",
        "version": "2.5.3",
    }
    r = requests.post(url, headers=headers, json=body, verify=False)
    token = r.json()["result"]["token"]
    appkey = r.json()["result"]["appKey"]
    appsecret = r.json()["result"]["appSecret"]
    cid = r.json()["result"]["cid"]
    refresh_tokens = r.json()["result"]["refreshToken"]
    return token, appkey, appsecret, cid, refresh_tokens


if __name__ == "__main__":
    a = app_token("https://dev.1stcs.cn", 18031160867, "TlRReE5tUTNZMlEyWldZeE9UVmhNR1kzTmpJeVlUbGpOVFppTlRWbE9EUT0=",
                  10)
    print(a)
