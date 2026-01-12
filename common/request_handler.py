import requests
from typing import Optional, Dict, Any
from common.logger import logger
class RequestHandler:
    """请求处理类"""

    def __init__(self, session: requests.Session):
        self.session = session

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求

        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 其他requests参数

        Returns:
            requests.Response对象
        """
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # 检查HTTP错误
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            raise

    def add_header(self, key: str, value: str):
        """添加公共请求头"""
        self.session.headers[key] = value

    def remove_header(self, key: str):
        """移除请求头"""
        if key in self.session.headers:
            del self.session.headers[key]

    def clear_headers(self):
        """清空所有请求头"""
        self.session.headers.clear()