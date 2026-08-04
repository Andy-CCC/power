# testcase/test_user.py

from api.user_api import UserApi
from common.assert_util import AssertUtil

class TestUser:
    # 以后所有的测试都这么写
    def test_get_user_info(self):
        response = UserApi().get_user_info()
        body = AssertUtil.assert_success(response)

    def test_get_banner(self):
        response = UserApi().get_banner()
        body = AssertUtil.assert_success(response)
