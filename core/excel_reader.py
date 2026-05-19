import openpyxl
import os
from config.env_config import BASE_DIR
from core.logger import log
#无需修改：excel用例读取
class ExcelReader:
    def __init__(self, file_name="api_cases.xlsx"):
        self.file_path = os.path.join(BASE_DIR, "test_data", file_name)
        # 检查Excel文件是否存在
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"用例文件不存在：{self.file_path}")
        self.workbook = openpyxl.load_workbook(self.file_path)

    def get_cases(self, sheet_name="Sheet1"):
        """读取用例，返回字典列表"""
        try:
            sheet = self.workbook[sheet_name]
            rows = list(sheet.iter_rows(values_only=True))
            if len(rows) < 2:
                log.warning("Excel用例表无数据")
                return []
            # 表头作为key
            headers = rows[0]
            cases = []
            for row in rows[1:]:
                if any(row):  # 跳过空行
                    cases.append(dict(zip(headers, row)))
            log.info(f"成功读取{len(cases)}条用例")
            return cases
        except Exception as e:
            log.error(f"读取Excel失败：{str(e)}")
            raise

# 全局实例
excel_reader = ExcelReader()