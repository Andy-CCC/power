import pymysql
from config.db_config import DB_CONFIG
from core.logger import log
#断言封装，无需修改
class AssertUtils:
    """通用断言工具：接口断言 + 数据库断言"""
    @staticmethod
    def assert_code(response, expect_code=200):
        """断言响应状态码"""
        real_code = response.status_code
        assert real_code == expect_code, f"状态码断言失败：预期{expect_code}，实际{real_code}"
        log.info(f"状态码断言成功：{real_code} == {expect_code}")

    @staticmethod
    def assert_json_value(response, key, expect_value):
        """断言JSON响应中的某个字段值"""
        try:
            resp_json = response.json()
            real_value = resp_json.get(key)
            assert real_value == expect_value, f"字段断言失败：{key}预期{expect_value}，实际{real_value}"
            log.info(f"字段断言成功：{key}={real_value}")
        except Exception as e:
            log.error(f"JSON字段断言失败：{str(e)}")
            raise

    @staticmethod
    def assert_db(sql, expect_value):
        """数据库断言（可选）"""
        if not sql or not expect_value:
            return
        try:
            # 连接数据库执行SQL
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            conn.close()

            real_value = result[0] if result else None
            assert real_value == expect_value, f"DB断言失败：预期{expect_value}，实际{real_value}"
            log.info(f"DB断言成功：{real_value} == {expect_value}")
        except Exception as e:
            log.error(f"数据库断言失败：{str(e)}")
            raise

# 实例化，全局使用
assert_utils = AssertUtils()