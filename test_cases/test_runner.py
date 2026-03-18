import pytest
import json
from core.excel_utils import excel_reader
from core.http_client import http_client
from core.assert_utils import assert_utils
from core.logger import log

#自动执行用例，无需修改
# 读取Excel中的用例数据
test_cases = excel_reader.get_cases()

class TestApiAuto:
    """接口自动化用例执行类"""
    @pytest.mark.parametrize("case", test_cases)
    def test_run_case(self, case):
        """执行单条用例"""
        # 解析用例数据（Excel中的列名需和这里对应）
        case_name = case.get("case_name")
        method = case.get("method")
        url = case.get("url")
        params = case.get("params")  # GET参数，JSON格式字符串
        json_data = case.get("json")  # POST参数，JSON格式字符串
        expect_code = case.get("expect_code")  # 预期状态码
        expect_key = case.get("expect_key")  # 预期字段名
        expect_value = case.get("expect_value")  # 预期字段值
        db_sql = case.get("db_sql")  # 数据库校验SQL
        db_expect = case.get("db_expect")  # 数据库预期值

        log.info(f"========== 执行用例：{case_name} ==========")
        # 转换参数格式（字符串转字典）
        params = json.loads(params) if params else None
        json_data = json.loads(json_data) if json_data else None
        expect_code = int(expect_code) if expect_code else 200

        # 发送请求
        response = http_client.send_request(method, url, params, json_data)

        # 接口断言
        assert_utils.assert_code(response, expect_code)
        if expect_key and expect_value:
            assert_utils.assert_json_value(response, expect_key, expect_value)

        # 数据库断言（可选）
        if db_sql and db_expect:
            assert_utils.assert_db(db_sql, db_expect)

        log.info(f"========== 用例{case_name}执行成功 ==========")