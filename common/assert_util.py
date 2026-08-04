# common/assert_util.py


class AssertUtil:

    @staticmethod
    def assert_success(response):
        """
        通用接口成功断言
        """

        # HTTP状态码
        assert response.status_code == 200, \
            f"HTTP状态码错误：{response.status_code}"

        # json数据
        body = response.json()

        # 业务状态码
        assert body["code"] == 0, \
            f"业务状态码错误：{body}"

        # 返回body，方便后续继续断言
        return body