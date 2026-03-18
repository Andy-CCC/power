import pytest
from core.logger import log

@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    """全局会话夹具：测试开始/结束提示"""
    log.info("======= 接口自动化测试开始 =======")
    yield
    log.info("======= 接口自动化测试结束 =======")