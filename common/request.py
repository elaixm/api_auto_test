import requests
import allure
from common.logger import logger
from config.settings import config


class Request:
    """requests二次封装：自动带BaseURL、自动带token、统一日志、异常捕获"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.base_url
        self.timeout = config.timeout
        # 默认请求头
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def set_token(self, token):
        """登录后调用，把token注入请求头"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info(f"Token已注入请求头: {token[:20]}...")

    def request(self, method, path, **kwargs):
        url = self.base_url + path
        kwargs.setdefault("timeout", self.timeout)

        logger.info(f"请求: {method.upper()} {url}")
        if "params" in kwargs:
            logger.info(f"  Query参数: {kwargs['params']}")
        if "json" in kwargs:
            logger.info(f"  Body: {kwargs['json']}")
        if "data" in kwargs:
            logger.info(f"  Form Data: {kwargs['data']}")

        try:
            resp = self.session.request(method, url, **kwargs)
            logger.info(f"响应状态码: {resp.status_code}")
            logger.info(f"响应体: {resp.text[:500]}")
            return resp
        except requests.RequestException as e:
            logger.error(f"请求异常: {e}")
            raise

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)


# 全局单例
http = Request()
