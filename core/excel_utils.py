import openpyxl
import os
from config.env_config import BASE_DIR
from core.logger import log
#Excel 用例读取，无需改
class ExcelReader:
    """读取Excel用例数据"""
    def __init__(self, file_name="api_cases.xlsx"):
        # Excel文件路径
        self.file_path = os.path.join(BASE_DIR, "test_data", file_name)
        # 加载Excel文件
        self.workbook = openpyxl.load_workbook(self.file_path)

    def get_cases(self, sheet_name="Sheet1"):
        """读取指定sheet的用例，返回字典列表"""
        try:
            sheet = self.workbook[sheet_name]
            # 获取所有行数据
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                log.warning("Excel用例表为空")
                return []
            # 表头作为key，后续行作为value
            headers = rows[0]
            cases = []
            for row in rows[1:]:
                if any(row):  # 跳过空行
                    cases.append(dict(zip(headers, row)))
            log.info(f"成功读取{len(cases)}条用例")
            return cases
        except Exception as e:
            log.error(f"读取Excel用例失败：{str(e)}")
            raise

# 实例化，全局使用
excel_reader = ExcelReader()