import requests
from config.env_config import BASE_URL, TIMEOUT, DEFAULT_HEADERS, TOKEN_HEADER, TOKEN_PREFIX
from core.logger import log

class HttpClient:
    def __init__(self, token=""):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        # 自动携带Token
        if token:
            self.session.headers[TOKEN_HEADER] = TOKEN_PREFIX + token

    def send_request(self, method, url, params=None, json=None):
        """统一发送请求"""
        full_url = BASE_URL + url
        log.info(f"【请求】环境：{BASE_URL} | 方法：{method} | 路径：{url}")
        log.info(f"【请求参数】params={params} | json={json}")

        try:
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                params=params,
                json=json,
                timeout=TIMEOUT
            )
            log.info(f"【响应】状态码：{response.status_code} | 内容：{response.text}")
            return response
        except Exception as e:
            log.error(f"【请求失败】{str(e)}")
            raise Exception(f"接口请求异常：{str(e)}")

# 核心补充：创建全局可调用的实例（其他模块直接导入这个实例）
http_client = HttpClient()