import allure
import pytest
from api.user_api import UserApi
from common.data_util import DataUtil
from common.assert_util import AssertUtil

# 加载用户消费记录测试数据
user_webGetSeriesDetailContent_data = DataUtil.get_case_data(
    "video_data.yaml",
    "user_webGetSeriesDetailContent_list"
)


class TestVideo:
    @allure.feature("播放器模块")
    @allure.story("播放器")
    @allure.title("短剧详情")
    @pytest.mark.parametrize("case", user_webGetSeriesDetailContent_data.values(),
                             ids=[
                                 item["case_name"]
                                 for item in user_webGetSeriesDetailContent_data.values()
                             ]
                             )
    @allure.title("{case[case_name]}")
    def test_get_user_spending_list(self, case):
        """
        获取用户消费记录接口
        """
        # Allure显示当前测试数据
        allure.attach(str(case), name="测试数据", attachment_type=allure.attachment_type.TEXT)
        response = UserApi().get_video_webGetSeriesDetailContent(
            series_id=case["series_id"],

        )
        # 校验HTTP状态码
        AssertUtil.assert_http_status(response)
        # 校验业务code
        AssertUtil.assert_code(response, case["expected_code"])
