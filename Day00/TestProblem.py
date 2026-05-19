import requests
import json


class APITest:
    """接口测试工具类"""
    def __init__(self, base_url):
        """
        初始化
        :param base_url: 接口基础地址
        """
        self.base_url = base_url
        self.session = requests.Session()
        # 通用请求头（可根据需要修改）
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "APITest/1.0"
        })
        # 存储提取的变量
        self.context = {}

    def request(self, method, path, **kwargs):
        """
        发送请求
        :param method: GET/POST/PUT/DELETE
        :param path: 接口路径
        :param kwargs: requests库的其他参数
        :return: 响应对象
        """
        url = self.base_url + path
        print(f"\n{'=' * 50}")
        print(f"请求: {method} {url}")
        print(f"参数: {kwargs.get('params', {})}")
        print(f"数据: {kwargs.get('json', {})}")

        response = self.session.request(method, url, **kwargs)
        print(f"响应状态: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        return response

    def assert_status(self, response, expected_status=200):
        """断言状态码"""
        assert response.status_code == expected_status, \
            f"状态码错误: 期望{expected_status}, 实际{response.status_code}"
        print(f"✓ 状态码验证通过: {expected_status}")

    def assert_json_field(self, response, field, expected_value=None):
        """
        断言JSON字段
        :param response: 响应对象
        :param field: 字段路径，如 "data.userId" 或 "code"
        :param expected_value: 期望值，不传则只验证字段存在
        """
        try:
            json_data = response.json()
        except:
            raise AssertionError("响应不是JSON格式")

        # 支持多层路径，如 "data.userId"
        keys = field.split('.')
        value = json_data
        for key in keys:
            assert key in value, f"字段 '{field}' 不存在"
            value = value[key]

        if expected_value is not None:
            assert value == expected_value, \
                f"字段 '{field}' 值错误: 期望{expected_value}, 实际{value}"

        print(f"✓ 字段 '{field}' 验证通过: {value}")
        return value

    def extract(self, field, var_name):
        """
        提取字段值到上下文
        :param field: 字段路径，如 "data.userId"
        :param var_name: 存储的变量名
        """
        response = self.context.get('_last_response')
        if not response:
            raise Exception("没有可提取的响应，请先调用接口")

        value = self.assert_json_field(response, field)
        self.context[var_name] = value
        print(f"✓ 提取变量: {var_name} = {value}")


# ==================== 使用示例 ====================

def main():
    # 1. 初始化（替换为你的接口地址）
    api = APITest(base_url="https://fas-api.flextv9.com")
    # ========== 场景：登录 → 获取用户信息 ==========
    # 第一步：登录接口（示例用公开API模拟）
    print("\n>>> 步骤1: 登录")
    response = api.request(
        method="POST",
        path="/admin/member/login",
        json={"tel":"18218410011","captcha":"8888","type":1}
    )
    api.context['_last_response'] = response  # 保存最新响应

    # 断言状态码
    api.assert_status(response, 200)

    # 断言返回字段（示例API返回id）
    post_id = api.assert_json_field(response, "token")

    # 提取post_id到上下文
    api.extract("id", "post_id")

    # ========== 第二步：用提取的id查询详情 ==========
    print("\n>>> 步骤2: 获取详情")

    # 从上下文取出变量
    post_id = api.context.get("post_id")

    # 用提取的id拼接路径
    response2 = api.request(
        method="GET",
        path=f"/posts/{post_id}"
    )
    api.context['_last_response'] = response2

    # 断言
    api.assert_status(response2, 200)
    api.assert_json_field(response2, "id", post_id)

    print("\n" + "=" * 50)
    print("✓ 测试完成！")
    print(f"最终上下文: {api.context}")


if __name__ == "__main__":
    main()