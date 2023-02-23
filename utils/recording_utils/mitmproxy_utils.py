import json
import os
import traceback
from datetime import datetime
from datetime import timezone

from mitmproxy import ctx
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster

from common.setting import Path
from utils.file_utils.yaml_utils import YamlUtils
from utils.file_utils.har_py_utils import move_py
from utils.log_utils.loguru_utils import Logger
from utils.recording_utils.async_call_utils import async_call

""""
通过录制生成har文件
调试版本: python3.6.8
        mitmproxy==5.3.0
        
mitmproxy版本超过6.0.0 / 6.0.1 / 6.0.2不支持

操作步骤：
        1.本机开启http、https代理（参考此文件config/config.yaml文件的record_info信息）
        2.修改config/config.yaml文件的record_info信息
"""


def flow_to_har(flow):
    '''
    将flow转换成har格式数据
    '''

    def fromat_cookies(l):
        """
            格式化cookies
        :param l:
        :return:
        """

        try:
            #  "" if isinstance(i[1], tuple) else i[1] 如果 i[1] 是元组则 将i[1] 赋值成 ""
            cookies_list = [{'name': i[0], 'value': "" if isinstance(i[1], tuple) else i[1]} for i in l]
            return cookies_list  # NameError: name 'CookieAttrs' is not defined
        except Exception:
            Logger().error(traceback.format_exc())

    def name_value(obj):

        try:
            return [{"name": k, "value": v} for k, v in obj.items()]
        except Exception:
            Logger().error(traceback.format_exc())

    try:
        HAR = {}
        # 合并字典
        HAR.update({
            "log": {
                "version": "1.2",
                "creator": {
                    "name": "mitmproxy har_dump",
                    "version": "0.1",
                    "comment": "mitmproxy"
                },
                "entries": []
            }
        })

        ssl_time = -1
        connect_time = -1

        if flow.server_conn and flow.server_conn:
            connect_time = (flow.server_conn.timestamp_tcp_setup -
                            flow.server_conn.timestamp_start)

            if flow.server_conn.timestamp_tls_setup is not None:
                ssl_time = (flow.server_conn.timestamp_tls_setup -
                            flow.server_conn.timestamp_tcp_setup)

        timings_raw = {
            'send': flow.request.timestamp_end - flow.request.timestamp_start,
            'receive': flow.response.timestamp_end - flow.response.timestamp_start,
            'wait': flow.response.timestamp_start - flow.request.timestamp_end,
            'connect': connect_time,
            'ssl': ssl_time,
        }

        timings = {
            k: int(1000 * v) if v != -1 else -1
            for k, v in timings_raw.items()
        }

        full_time = sum(v for v in timings.values() if v > -1)

        started_date_time = datetime.fromtimestamp(flow.request.timestamp_start, timezone.utc).isoformat()

        response_body_size = len(flow.response.raw_content) if flow.response.raw_content else 0
        response_body_decoded_size = len(flow.response.content) if flow.response.content else 0
        response_body_compression = response_body_decoded_size - response_body_size

        entry = {
            "startedDateTime": started_date_time,
            "time": full_time,
            "request": {
                "method": flow.request.method,
                "url": flow.request.url,
                "httpVersion": flow.request.http_version,
                "cookies": fromat_cookies(flow.request.cookies.fields),
                "headers": name_value(flow.request.headers),
                "queryString": name_value(flow.request.query or {}),
                "headersSize": len(str(flow.request.headers)),
                "bodySize": len(flow.request.content),
            },
            "response": {
                "status": flow.response.status_code,
                "statusText": flow.response.reason,
                "httpVersion": flow.response.http_version,
                "cookies": fromat_cookies(flow.response.cookies.fields),
                "headers": name_value(flow.response.headers),
                "content": {
                    "size": response_body_size,
                    "compression": response_body_compression,
                    "mimeType": flow.response.headers.get('Content-Type', '')
                },
                "redirectURL": flow.response.headers.get('Location', ''),
                "headersSize": len(str(flow.response.headers)),
                "bodySize": response_body_size,
            },
            "cache": {},
            "timings": timings,
        }

        entry["response"]["content"]["text"] = flow.response.get_text(strict=False)

        if flow.request.method in ["POST", "PUT", "PATCH"]:
            params = [
                {"name": a, "value": b}
                for a, b in flow.request.urlencoded_form.items(multi=True)
            ]
            entry["request"]["postData"] = {
                "mimeType": flow.request.headers.get("Content-Type", ""),
                "text": flow.request.get_text(strict=False),
                "params": params
            }

        if flow.server_conn.connected:
            entry["serverIPAddress"] = str(flow.server_conn.ip_address[0])

        HAR["log"]["entries"].append(entry)
        urls = flow.request.path
        strs = urls
        head, sep, tail = strs.partition('?')

        # url = flow.request.path.replace('/', '') \
        #     .replace('?', '').replace('&', '').replace('.', '').replace('=', '').replace(',', '') \
        #     .replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '') \
        #     .replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '') \
        #     .replace('-', '').replace('!', '').replace('$', '').replace('*', '').replace('`', '') \
        #     .replace('~', '').replace(';', '').replace(':', '').replace('"', '').replace("'", "") \
        #     .replace("%", "").replace("@", "").replace("#", "").replace("$", "").replace("^", "") \
        #     .replace("(", "").replace(")", "").replace("_", "").replace("[", "").replace("]", "") \
        #     .replace("{", "").replace("}", "").replace("|", "").replace("config", "")

        # 返回url，作为har文件的名称，get请求通过？切割，否则url的参数也会作为名称命名，不是我想要的，名称太长了
        url = flow.request.path.replace('/', '').split('?')[0]
        return HAR, url, head
    except Exception:
        Logger().error(traceback.format_exc())


class Test:
    def __init__(self, filter_url: str, filepath: str):
        """
        初始化方法
        :params filter_url: 指定抓取包含xx的接口请求
        :params filepath: 指定生成的har文件保存文件夹
        """
        self.filter_url = filter_url
        self.file_path = filepath

    def response(self, flow):
        """
        在response事件中写处理逻辑
        """
        try:
            # 过滤url，只抓取 包含 filter_url 的接口请求 并且 接口响应content-type 包含json的
            if self.filter_url in flow.request.url and ('json' in flow.response.headers.get('Content-Type', '')):
                har, url, head = flow_to_har(flow)

                msg = json.dumps(har, ensure_ascii=False)
                ctx.log.info('flow转化har格式数据')
                # ctx.log.info(msg)
                filename = f"{self.file_path}{os.sep}{url}.har"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(msg)

                # 生成har文件，并移动
                self.copy(filename)

            else:
                ctx.log.debug(flow.request.url)
        except Exception:
            Logger().error(traceback.format_exc())

    @async_call  # 多线程copy，否则会影响页面操作速度
    def copy(self, filename):

        # 将har文件转换为.py文件
        os.system(f"har2case\t{filename}")  # 将har文件转换为py文件

        # 移动har保存目录下的.py文件
        move_py(self.file_path)


def runtest():
    config_result = YamlUtils().read_yaml(Path.common_path + "config.yaml")
    url = config_result['record_info']['host']  # 包含该地址的接口 才会被捕获
    file_path = Path.har_path + config_result['record_info']['path']  # 文件保存的目录
    if not os.path.exists(file_path):
        # 创建多级目录
        os.makedirs(file_path)
    opts = options.Options(listen_host=config_result['record_info']['listen_host'],
                           listen_port=config_result['record_info']['listen_port'])
    opts.add_option("body_size_limit", int, 0, "")
    pconf = proxy.config.ProxyConfig(opts)
    # m = WebMaster(None)
    m = DumpMaster(None)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(Test(url, file_path))  # m.addons.add(Test(url, file_path))

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()
        Logger().error(traceback.format_exc())


if __name__ == "__main__":
    runtest()
