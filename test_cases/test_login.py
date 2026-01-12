import pytest
import allure
from common.base_api import BaseAPI
from common.assertion import Assertion
from common.utils import Utils


@allure.feature("登录模块")
class TestLogin(BaseAPI):
    """登录测试用例"""

    @allure.story("用户登录")
    @allure.title("测试正常登录")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self):
        """测试正常登录"""
        # 准备测试数据
        login_data = {
            "username": "admin",
            "password": "admin123"
        }

        # 发送请求
        response = self.post("/api/login", json=login_data)

        # 断言
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, {"code": 0, "message": "success"})

        # 验证返回的token
        response_json = response.json()
        assert "data" in response_json
        assert "token" in response_json["data"]
        assert len(response_json["data"]["token"]) > 0

    @allure.story("用户登录")
    @allure.title("测试密码错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        """测试密码错误"""
        login_data = {
            "username": "admin",
            "password": "wrong_password"
        }

        response = self.post("/api/login", json=login_data)

        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, {
            "code": 1001,
            "message": "用户名或密码错误"
        })

    @allure.story("用户登录")
    @allure.title("测试用户不存在")
    def test_login_user_not_exist(self):
        """测试用户不存在"""
        login_data = {
            "username": Utils.generate_random_string(10),
            "password": "any_password"
        }

        response = self.post("/api/login", json=login_data)

        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, {
            "code": 1002,
            "message": "用户不存在"
        })

    @allure.story("用户登录")
    @allure.title("测试参数缺失")
    @pytest.mark.parametrize("missing_field", ["username", "password"])
    def test_login_missing_parameters(self, missing_field):
        """测试参数缺失"""
        login_data = {
            "username": "admin",
            "password": "admin123"
        }

        # 移除指定的字段
        del login_data[missing_field]

        response = self.post("/api/login", json=login_data)

        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, {
            "code": 1003,
            "message": f"缺少参数: {missing_field}"
        })


@allure.feature("用户管理")
class TestUserManagement(BaseAPI):
    """用户管理测试用例"""

    def setup_class(self):
        """测试类初始化"""
        # 先登录获取token
        login_response = self.post("/api/login", json={
            "username": "admin",
            "password": "admin123"
        })

        self.token = login_response.json()["data"]["token"]
        self.headers["Authorization"] = f"Bearer {self.token}"

    @allure.story("获取用户列表")
    def test_get_user_list(self):
        """测试获取用户列表"""
        response = self.get("/api/users", params={"page": 1, "size": 10})

        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_schema(response, {
            "type": "object",
            "properties": {
                "code": {"type": "integer"},
                "message": {"type": "string"},
                "data": {
                    "type": "object",
                    "properties": {
                        "total": {"type": "integer"},
                        "users": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "username": {"type": "string"},
                                    "email": {"type": "string"}
                                },
                                "required": ["id", "username", "email"]
                            }
                        }
                    },
                    "required": ["total", "users"]
                }
            },
            "required": ["code", "message", "data"]
        })

    @allure.story("创建用户")
    def test_create_user(self):
        """测试创建用户"""
        user_data = {
            "username": Utils.generate_random_string(8),
            "email": Utils.generate_random_email(),
            "password": "Test123456"
        }

        response = self.post("/api/users", json=user_data)

        Assertion.assert_status_code(response, 201)
        response_json = response.json()

        # 验证返回的数据
        assert response_json["data"]["username"] == user_data["username"]
        assert response_json["data"]["email"] == user_data["email"]
        assert "id" in response_json["data"]

        # 保存用户ID供后续测试使用
        self.created_user_id = response_json["data"]["id"]

    @allure.story("删除用户")
    def test_delete_user(self):
        """测试删除用户"""
        # 先创建用户
        user_data = {
            "username": Utils.generate_random_string(8),
            "email": Utils.generate_random_email(),
            "password": "Test123456"
        }

        create_response = self.post("/api/users", json=user_data)
        user_id = create_response.json()["data"]["id"]

        # 删除用户
        response = self.delete(f"/api/users/{user_id}")

        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, {
            "code": 0,
            "message": "用户删除成功"
        })