import pytest
import allure
import os
from datetime import datetime
from config.config import config


def pytest_configure(config):
    """pytest配置"""
    # 设置环境变量
    os.environ['API_TEST_ENV'] = config.getoption("--env", "test")

    # 创建报告目录
    config.REPORT_DIR.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="测试环境: dev, test, prod"
    )
    parser.addoption(
        "--report",
        action="store",
        default="html",
        help="报告类型: html, xml, allure"
    )


@pytest.fixture(scope="session")
def api_client():
    """API客户端fixture"""
    from common.base_api import BaseAPI
    return BaseAPI()


@pytest.fixture(scope="function")
def setup_data():
    """测试数据准备"""
    from common.utils import Utils
    return {
        "timestamp": Utils.generate_timestamp(),
        "random_string": Utils.generate_random_string()
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告钩子"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 失败时截图（如果需要）
        pass