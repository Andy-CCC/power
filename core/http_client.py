import requests
import hashlib
from config.env_config import BASE_URL, TIMEOUT, DEFAULT_HEADERS, TOKEN, TOKEN_HEADER, IS_SIGN, APP_SECRET
from core.logger import log
#请求封装，无需改
class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        # 设置默认请求头
        self.session.headers.update(DEFAULT_HEADERS)
        # 自动携带Token
        if TOKEN:
            self.session.headers.update({TOKEN_HEADER: TOKEN})

    # 生成接口签名（MD5）
    def _generate_sign(self, data):
        if not data:
            return ""
        # 按key排序后拼接，再加秘钥
        sorted_data = sorted(data.items())
        sign_str = "".join([f"{k}{v}" for k, v in sorted_data]) + APP_SECRET
        # MD5加密并转大写
        return hashlib.md5(sign_str.encode()).hexdigest().upper()

    # 统一请求方法
    def send_request(self, method, url, params=None, json=None):
        full_url = BASE_URL + url
        # 开启签名时，自动给json参数加sign字段
        if IS_SIGN and json:
            json["sign"] = self._generate_sign(json)

        # 日志记录请求信息
        log.info(f"【请求】方法：{method} | URL：{full_url}")
        log.info(f"【请求】参数：params={params} | json={json}")

        try:
            # 发送请求
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                params=params,
                json=json,
                timeout=TIMEOUT
            )
            # 日志记录响应信息
            log.info(f"【响应】状态码：{response.status_code} | 内容：{response.text}")
            return response
        except Exception as e:
            log.error(f"【请求失败】{str(e)}")
            raise Exception(f"接口请求异常：{str(e)}")

# 实例化，全局使用
http_client = HttpClient()