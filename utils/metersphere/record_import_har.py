import json
import traceback
from datetime import datetime
from datetime import timezone
from threading import Thread

from mitmproxy import ctx
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster

from utils.log.loguru_utils import Logger
from utils.metersphere.import_har import ImportHar


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


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

    try:
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

        url = flow.request.path.replace('/', '') \
            .replace('?', '').replace('&', '').replace('.', '').replace('=', '').replace(',', '') \
            .replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '') \
            .replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '') \
            .replace('-', '').replace('!', '').replace('$', '').replace('*', '').replace('`', '') \
            .replace('~', '').replace(';', '').replace(':', '').replace('"', '').replace("'", "") \
            .replace("%", "").replace("@", "").replace("#", "").replace("$", "").replace("^", "") \
            .replace("(", "").replace(")", "").replace("_", "").replace("[", "").replace("]", "") \
            .replace("{", "").replace("}", "").replace("|", "").replace("config", "")

        return HAR, url, head
    except Exception:
        Logger().error(traceback.format_exc())


class Test:
    def __init__(self, filter_url: str):
        """
        初始化方法
        :params filter_url: 指定抓取包含xx的接口请求
        """
        self.filter_url = filter_url

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
                ctx.log.info(msg)
                filename = f"{url}.har"

                # 给ms平台导入har
                self.ms_har(filename, har)
            else:
                ctx.log.debug(flow.request.url)
        except Exception:
            Logger().error(traceback.format_exc())

    @async_call
    def ms_har(self, filename, msg):
        # 这是给ms平台接口定义模块录制导入har
        ImportHar().metersphere_definition_import_har(filename, msg)

        # 这是给ms平台接口自动化模块录制导入har
        # ImportHar().metersphere_automation_import_har(filename, msg)


def runtest():
    url = "https://dev.1stcs.cn"  # 包含该地址的接口 才会被捕获
    opts = options.Options(listen_host="127.0.0.1",
                           listen_port=8889)
    opts.add_option("body_size_limit", int, 0, "")
    pconf = proxy.config.ProxyConfig(opts)
    # m = WebMaster(None)
    m = DumpMaster(None)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(Test(url))  # m.addons.add(Test(url, file_path))

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()
        Logger().error(traceback.format_exc())


if __name__ == "__main__":
    runtest()
