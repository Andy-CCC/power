import json
from typing import Any, Dict, List, Union
import jsonschema
from deepdiff import DeepDiff

class Assertion:
    """断言工具类"""

    @staticmethod
    def assert_status_code(response, expected_code: int):
        """断言状态码"""
        assert response.status_code == expected_code, \
            f"状态码错误: 期望{expected_code}, 实际{response.status_code}"

    @staticmethod
    def assert_response_time(response, max_time: float):
        """断言响应时间"""
        actual_time = response.elapsed.total_seconds()
        assert actual_time <= max_time, \
            f"响应时间超时: 期望{max_time}秒内, 实际{actual_time}秒"

    @staticmethod
    def assert_json_contains(response, expected_data: Dict[str, Any]):
        """断言JSON响应包含特定数据"""
        actual_data = response.json()
        for key, value in expected_data.items():
            assert key in actual_data, f"响应中缺少键: {key}"
            assert actual_data[key] == value, \
                f"键'{key}'的值不匹配: 期望{value}, 实际{actual_data[key]}"

    @staticmethod
    def assert_json_schema(response, schema: Dict[str, Any]):
        """断言JSON响应符合schema"""
        try:
            jsonschema.validate(instance=response.json(), schema=schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON Schema验证失败: {str(e)}")

    @staticmethod
    def assert_equal(actual, expected, msg: str = ""):
        """断言相等"""
        assert actual == expected, f"{msg} 期望: {expected}, 实际: {actual}"

    @staticmethod
    def assert_not_equal(actual, expected, msg: str = ""):
        """断言不相等"""
        assert actual != expected, f"{msg} 值不应该相等: {actual}"

    @staticmethod
    def assert_in(item, container, msg: str = ""):
        """断言包含"""
        assert item in container, f"{msg} {item} 不在 {container} 中"

    @staticmethod
    def assert_not_in(item, container, msg: str = ""):
        """断言不包含"""
        assert item not in container, f"{msg} {item} 不应该在 {container} 中"

    @staticmethod
    def assert_true(expr, msg: str = ""):
        """断言为True"""
        assert expr, f"{msg} 期望为True, 实际为False"

    @staticmethod
    def assert_false(expr, msg: str = ""):
        """断言为False"""
        assert not expr, f"{msg} 期望为False, 实际为True"

    @staticmethod
    def assert_json_equal(actual_json, expected_json, ignore_order: bool = False):
        """
        深度比较两个JSON对象

        Args:
            actual_json: 实际JSON
            expected_json: 期望JSON
            ignore_order: 是否忽略列表顺序
        """
        diff = DeepDiff(
            expected_json,
            actual_json,
            ignore_order=ignore_order,
            exclude_paths=["root['timestamp']", "root['id']"]  # 排除动态字段
        )

        if diff:
            raise AssertionError(f"JSON不匹配: {json.dumps(diff, indent=2, ensure_ascii=False)}")