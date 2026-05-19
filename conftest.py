import pytest
import time
from core.logger import log
from core.http_client import HttpClient
from config.env_config import LOGIN_URL, LOGIN_PARAMS, BASE_URL

# 全局初始化HttpClient实例（关键：先实例化，再赋值Token）
global_client = HttpClient()


@pytest.fixture(scope="session", autouse=True)
def get_global_token():
    """会话级夹具：登录获取Token，全局生效"""
    log.info(f"======= 开始登录【{BASE_URL}】=======")
    login_client = HttpClient()
    # 登录重试（3次）
    for retry in range(3):
        try:
            # 发送登录请求
            response = login_client.send_request("POST", LOGIN_URL, json=LOGIN_PARAMS)
            # 断言登录成功
            assert response.status_code == 200, f"登录状态码异常：{response.status_code}"
            resp_json = response.json()
            # 提取Token（根据公司接口返回调整，示例：{"data":{"token":"xxx"}}）
            token = resp_json["data"]["token"]
            assert token, "登录成功但无Token"

            # 正确给全局实例添加Token（核心修复！）
            global_client.session.headers["Authorization"] = token  # 替换为你的TOKEN_HEADER
            log.info(f"======= 登录成功，Token：{token} =======")
            return token
        except Exception as e:
            if retry == 2:
                log.error(f"登录重试3次失败，终止测试：{str(e)}")
                pytest.exit(f"登录失败：{str(e)}")
            log.warning(f"登录重试{retry + 1}次失败：{str(e)}，1秒后重试")
            time.sleep(1)


@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    """测试会话开始/结束提示"""
    log.info("======= 接口自动化测试开始 =======")
    yield
    log.info("======= 接口自动化测试结束 =======")