# api/base_api.py

import time
import requests

from common.config import BASE_URL
from common.headers import get_headers
from common.logger import logger


class BaseApi:
    """接口基类"""

    def __init__(self):
        # 创建 Session，提高请求效率
        self.session = requests.Session()

        # 不使用系统代理（避免 ProxyError）
        self.session.trust_env = False

    def send(self, method, path, name="", **kwargs):
        """
        公共请求方法

        :param method: 请求方式(GET/POST/PUT/DELETE)
        :param path: 接口路径
        :param name: 接口名称（日志展示）
        :param kwargs:
            params=
            json=
            data=
            files=
        :return: Response
        """

        url = BASE_URL + path
        headers = get_headers()

        try:
            # ================= 请求日志 =================
            logger.info("=" * 80)

            if name:
                logger.info(f"接口名称：{name}")

            logger.info(f"请求地址：{url}")
            logger.info(f"请求方式：{method}")
            logger.info(f"请求请求头：{headers}")

            if "params" in kwargs:
                logger.info(f"请求参数(params)：{kwargs['params']}")

            if "json" in kwargs:
                logger.info(f"请求参数(json)：{kwargs['json']}")

            if "data" in kwargs:
                logger.info(f"请求参数(data)：{kwargs['data']}")

            # 开始计时
            start_time = time.perf_counter()

            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=10,
                **kwargs
            )

            # 结束计时
            end_time = time.perf_counter()

            elapsed_ms = round((end_time - start_time) * 1000, 2)

            # 保存响应时间，方便测试断言
            response.elapsed_ms = elapsed_ms

            # ================= 响应日志 =================
            logger.info(f"HTTP状态码：{response.status_code}")
            logger.info(f"接口响应时间：{elapsed_ms} ms")

            try:
                logger.info(f"响应结果：{response.json()}")
            except Exception:
                logger.info(f"响应结果：{response.text}")

            logger.info("=" * 80)

            return response

        except requests.exceptions.Timeout:
            logger.error("接口请求超时！")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"接口请求异常：{e}")
            raise

    # ================= GET =================

    def get(self, path, name="", **kwargs):
        return self.send(
            method="GET",
            path=path,
            name=name,
            **kwargs
        )

    # ================= POST =================

    def post(self, path, name="", **kwargs):
        return self.send(
            method="POST",
            path=path,
            name=name,
            **kwargs
        )

    # ================= PUT =================

    def put(self, path, name="", **kwargs):
        return self.send(
            method="PUT",
            path=path,
            name=name,
            **kwargs
        )

    # ================= DELETE =================

    def delete(self, path, name="", **kwargs):
        return self.send(
            method="DELETE",
            path=path,
            name=name,
            **kwargs
        )