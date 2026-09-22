import allure


class AssertUtil:
    """
    接口断言工具类

    说明：
    1. 通用断言放这里
    2. 业务特殊字段由测试用例自己决定
    3. 不强制校验data字段
    """

    @staticmethod
    def assert_http_status(response, expect=200):
        """
        校验HTTP状态码
        """

        with allure.step(
                f"校验HTTP状态码={expect}"
        ):

            actual = response.status_code

            assert actual == expect, (
                f"HTTP状态码错误\n"
                f"预期：{expect}\n"
                f"实际：{actual}"
            )


    @staticmethod
    def assert_code(response, expect=0):
        """
        校验业务code

        示例：
        {
            "code":0,
            "msg":"success"
        }
        """

        body = response.json()

        with allure.step(
                f"校验业务code={expect}"
        ):

            actual = body.get("code")


            assert actual == expect, (
                f"业务code错误\n"
                f"预期：{expect}\n"
                f"实际：{actual}\n"
                f"响应：{body}"
            )



    @staticmethod
    def assert_message(response, expect=None):
        """
        校验msg字段

        非所有接口必须使用
        """

        body = response.json()


        with allure.step(
                f"校验msg={expect}"
        ):

            actual = body.get("msg")


            assert actual == expect, (
                f"msg错误\n"
                f"预期：{expect}\n"
                f"实际：{actual}"
            )



    @staticmethod
    def assert_field_exists(response, field):
        """
        校验响应字段存在

        例如：
        data
        list
        total
        """

        body = response.json()


        with allure.step(
                f"校验字段存在：{field}"
        ):

            assert field in body, (
                f"响应缺少字段：{field}\n"
                f"当前响应：{body}"
            )



    @staticmethod
    def assert_field_not_empty(response, field):
        """
        校验字段非空

        适用于：
        data密文
        token
        id
        """

        body = response.json()


        with allure.step(
                f"校验字段非空：{field}"
        ):

            value = body.get(field)


            assert value not in [
                None,
                ""
            ], (
                f"字段为空：{field}"
            )



    @staticmethod
    def assert_json_type(response):
        """
        校验响应是否为JSON
        """

        with allure.step(
                "校验响应格式JSON"
        ):

            try:
                response.json()

            except Exception:

                assert False, (
                    "响应不是JSON格式\n"
                    f"响应内容：{response.text}"
                )