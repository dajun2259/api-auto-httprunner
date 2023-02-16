import time

import requests
from httprunner import __version__

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils
from web_Login import web_token

config = YamlUtils().read_yaml(Path.config_path + "config.yaml")
print(config)


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


def setup_hooks_request(request=None):
    """

    :param request:
    """
    if config['api_type'] == "web":
        web_header_replace(request)

    elif config['api_type'] == "app":
        app_header_replace(request)


def web_header_replace(request):
    """
    替换请求header
    :param request:
    :return:
    """

    global url, tenantid, secret_code

    if "https://test.1stcs.cn" in request["url"]:
        url = "https://test.1stcs.cn"
        tenantid = config['login_config']['test_tenantId']

    elif "https://dev.1stcs.cn" in request["url"]:
        url = "https://dev.1stcs.cn"
        tenantid = config['login_config']['dev_tenantId']

    datas = web_token(url, config['login_config']['user_name'], config['login_config']['user_pass'],
                      tenantid)

    times = timestamps()
    get_re_appKey = datas[1]

    '''Hook更改Headers请求'''
    timess = {"x-timestamp": times}
    authorization = {"authorization": datas[0]}
    x_user_token = {"x-user-token": datas[0]}
    admin_token = {"Admin-Token": datas[0]}
    appkey = {"x-appkey": get_re_appKey}
    header = {'Content-Type': 'application/json'}

    if 'headers' in request:
        if bool(request['headers']) is True:
            header = request["headers"]
            if "authorization" in header:
                request['headers'].update(authorization)
            else:
                pass
            if "x-appkey" in header:
                request['headers'].update(appkey)
            else:
                pass
            if "x-timestamp" in header:
                request['headers'].update(timess)
            else:
                pass
            if "x-secret-code" in header:
                request['headers'].update(secret_code)
            else:
                pass
            if "x-user-token" in header:
                request['headers'].update(x_user_token)
            else:
                pass
            if "x-tid" in header:
                request['headers'].update({"x-tid": str(tenantid)})
            else:
                pass
            if "tenantid" in header:
                request['headers'].update({"tenantid": str(tenantid)})
            else:
                pass

        else:
            request['headers'].update(header)
    else:
        request['headers'] = header

    '''Hook更改请求参数中的cookies请求'''
    if 'cookies' in request:
        if bool(request['cookies']) is True:
            request['cookies'].update(admin_token)
        else:
            pass


def app_header_replace(request):
    """

    :param request:
    :return:
    """
    pass


def teardown_assert_response(response):
    """

    :param response:
    :return:
    """
    if response.status_code == 200 or 201:
        if response.body['status'] == 1:
            print('接口访问成功')
    else:
        print('接口请求失败')
    print('后置条件执行完成')


def upload_ticket(baseurl, filename):
    """

    :param baseurl:
    :param filename:
    :return:
    """
    global url, tenantid, m

    filepath = Path.attach_path + filename

    timestamp = int(round(time.time() * 1000))

    if "https://test.1stcs.cn" in baseurl:
        url = "https://test.1stcs.cn"
        tenantId = config['login_config']['test_tenantId']
    elif "https://dev.1stcs.cn" in baseurl:
        url = "https://dev.1stcs.cn"
        tenantId = config['login_config']['dev_tenantId']

    datas = web_token(url, config['login_config']['user_name'], config['login_config']['user_pass'],
                      tenantid)
    token = datas[0]
    appKey = datas[1]

    url2 = url + "/webportal/upload/ticket"
    header = {
        "accept": "application/json, text/plain, */*",
        "authorization": token,
        "tenantid": str(tenantid),
        "x-appkey": appKey,
        "x-tid": str(tenantid),
        "x-tz": str(-8),
        "x-user-token": token
    }

    if filepath.split(".")[-1] in ["jpg", "jpeg"]:

        m = {"file": (f"{timestamp}.jpeg", open(filepath, "rb"), "image/jpeg")

             }
    elif filepath.split(".")[-1] == "png":
        m = {"file": (f"{timestamp}.png", open(filepath, "rb"), "image/png")

             }
    else:
        print("附件上传暂时支持jpeg、jpeg、png")

    r = requests.post(url=url2, files=m, headers=header, verify=False)
    return r.json()["result"][0]


if __name__ == '__main__':
    # a = upload_ticket("https://test.1stcs.cn", "王者荣耀寅虎心曲杨玉环 无水印4k游戏壁纸_彼岸图网.jpg")
    a = timestamps()
    print(a)
