import pytest
import allure
import yaml
import os
from config.settings import config
from api.user_api import UserAPI
from utils.extract import Extractor
from common.logger import logger


def load_yaml(filename):
    """加载data目录下的YAML测试数据"""
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """
    会话级前置：整个测试session只执行一次
    1. 清空依赖缓存
    2. 登录普通用户，获取token
    """
    Extractor.clear()
    account = config.get_account("normal_user")
    logger.info(f"=== 测试开始，环境: {config.env}，登录用户: {account['username']} ===")

    with allure.step("前置：用户登录获取token"):
        resp = UserAPI.login(account["username"], account["password"])
        assert resp.status_code == 200, f"登录失败，状态码={resp.status_code}"
        token = Extractor.get("token")
        assert token, "登录后未获取到token"

    yield  # 所有用例执行

    logger.info("=== 测试结束 ===")
