import json
import time
import allure
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.config import config
from common.logger import logger
from common.request_handler import RequestHandler


class BaseAPI:
    """API请求基类"""

    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = self._create_session()
        self.request_handler = RequestHandler(self.session)
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'API-Test-Framework/1.0'
        }

    def _create_session(self):
        """创建带有重试机制的session"""
        session = requests.Session()

        # 设置重试策略
        retry_strategy = Retry(
            total=config.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        logger.info(f"请求方法: {method}")
        logger.info(f"请求URL: {url}")
        if 'json' in kwargs:
            logger.info(f"请求体: {json.dumps(kwargs['json'], ensure_ascii=False)}")
        if 'params' in kwargs:
            logger.info(f"请求参数: {kwargs['params']}")
        if 'headers' in kwargs:
            logger.info(f"请求头: {kwargs['headers']}")

    def _log_response(self, response: requests.Response):
        """记录响应日志"""
        logger.info(f"响应状态码: {response.status_code}")
        try:
            logger.info(f"响应体: {json.dumps(response.json(), ensure_ascii=False)}")
        except:
            logger.info(f"响应体: {response.text}")
        logger.info(f"响应时间: {response.elapsed.total_seconds()}秒")

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"

        # 合并headers
        headers = self.headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers

        # 设置超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = config.TIMEOUT

        # 记录请求
        self._log_request(method, url, **kwargs)

        # 发送请求
        start_time = time.time()
        response = self.request_handler.request(method, url, **kwargs)
        end_time = time.time()

        # 记录响应
        self._log_response(response)

        # Allure报告记录
        allure.attach(f"请求URL: {url}", name="请求URL")
        allure.attach(f"请求方法: {method}", name="请求方法")
        if 'json' in kwargs:
            allure.attach(json.dumps(kwargs['json'], indent=2, ensure_ascii=False),
                          name="请求体")
        allure.attach(json.dumps(dict(response.headers), indent=2), name="响应头")
        allure.attach(json.dumps(response.json(), indent=2, ensure_ascii=False),
                      name="响应体")
        allure.attach(f"响应时间: {end_time - start_time:.2f}秒", name="响应时间")

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('DELETE', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('PATCH', endpoint, **kwargs)