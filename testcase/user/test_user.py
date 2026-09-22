import allure
import pytest
from api.user_api import UserApi
from common.data_util import DataUtil
from common.assert_util import AssertUtil

# 加载用户消费记录测试数据
user_spending_data = DataUtil.get_case_data(
    "user_data.yaml",
    "user_spending_list"
)
user_webUserTopUp_data = DataUtil.get_case_data(
    "user_data.yaml",
    "user_webUserTopUp_list"
)
class TestUser:
    """
    用户模块测试
    """

    @allure.feature("用户模块")
    @allure.story("个人信息")
    @allure.title("获取个人信息接口")
    def test_get_user_info(self):
        """
        获取个人信息
        """
        response = UserApi().get_user_info()
        # 校验HTTP状态码
        AssertUtil.assert_http_status(response)
        # 校验业务code
        AssertUtil.assert_code(response, 0)

    @allure.feature("用户模块")
    @allure.story("我的钱包")
    @pytest.mark.parametrize("case", user_spending_data.values(),
                             ids=[
                                 item["case_name"]
                                 for item in user_spending_data.values()
                             ]
                             )
    @allure.title("{case[case_name]}")
    def test_get_user_spending_list(self, case):
        """
        获取用户消费记录接口
        """
        # Allure显示当前测试数据
        allure.attach(str(case), name="测试数据", attachment_type=allure.attachment_type.TEXT)
        response = UserApi().get_user_spending_list(
            page_no=case["page_no"],
            page_size=case["page_size"]
        )
        # 校验HTTP状态码
        AssertUtil.assert_http_status(response)
        # 校验业务code
        AssertUtil.assert_code(response, case["expected_code"])

    @allure.feature("用户模块")
    @allure.story("我的钱包")
    @pytest.mark.parametrize("case", user_webUserTopUp_data.values(),
                             ids=[
                                 item["case_name"]
                                 for item in user_webUserTopUp_data.values()
                             ]
                             )
    @allure.title("{case[case_name]}")
    def test_get_user_webUserTopUp_list(self, case):
        """
        获取用户充值记录接口
        """
        # Allure显示当前测试数据
        allure.attach(str(case), name="测试数据", attachment_type=allure.attachment_type.TEXT)
        response = UserApi().get_user_spending_list(page_no=case["page_no"], page_size=case["page_size"])
        # 校验HTTP状态码
        AssertUtil.assert_http_status(response)
        # 校验业务code
        AssertUtil.assert_code(response, case["expected_code"])
