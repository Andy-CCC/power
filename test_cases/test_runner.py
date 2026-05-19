import pytest
import json
import allure
from core.excel_reader import excel_reader
from core import http_client
from core.assert_utils import assert_utils
from core.logger import log
#无需改：用例执行
# 读取Excel用例
test_cases = excel_reader.get_cases()

@allure.epic(f"【{http_client.session.base_url}】接口自动化测试")
class TestApiAuto:
    @pytest.mark.parametrize("case", test_cases)
    def test_run_case(self, case):
        """执行单条用例"""
        # 解析用例
        case_name = case.get("case_name")
        method = case.get("method")
        url = case.get("url")
        params = case.get("params")
        json_data = case.get("json")
        expect_code = case.get("expect_code")
        expect_key = case.get("expect_key")
        expect_value = case.get("expect_value")
        db_sql = case.get("db_sql")
        db_expect = case.get("db_expect")

        log.info(f"========== 执行用例：{case_name} ==========")
        # 转换参数格式
        params = json.loads(params) if params else None
        json_data = json.loads(json_data) if json_data else None
        expect_code = int(expect_code) if expect_code else 200

        # Allure报告定制
        allure.dynamic.feature(case.get("module", "默认模块"))  # 接口模块
        allure.dynamic.story(case_name)                       # 用例名
        allure.dynamic.severity(case.get("level", "normal"))  # 优先级
        allure.dynamic.description(f"""
        <h3>接口信息</h3>
        <p>请求方法：{method}</p>
        <p>接口路径：{url}</p>
        <p>请求参数：params={params} | json={json_data}</p>
        <h3>断言信息</h3>
        <p>预期状态码：{expect_code}</p>
        <p>预期字段：{expect_key} = {expect_value}</p>
        <p>数据库校验：{db_sql} → {db_expect}</p>
        """, escape=False)

        # 发送请求
        response = http_client.send_request(method, url, params, json_data)

        # 执行断言
        assert_utils.assert_code(response, expect_code)
        if expect_key and expect_value:
            assert_utils.assert_json(response, expect_key, expect_value)
        if db_sql and db_expect:
            assert_utils.assert_db(db_sql, db_expect)

        log.info(f"========== 用例{case_name}执行成功 ==========")