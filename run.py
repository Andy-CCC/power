import pytest
import os
from config.env_config import BASE_DIR

if __name__ == "__main__":
    # 执行pytest用例
    pytest.main()
    # 生成Allure报告
    allure_report_dir = os.path.join(BASE_DIR, "reports", "allure-report")
    os.system(f"allure generate ./reports/allure-results -o {allure_report_dir} --clean")
    # 自动打开报告（仅Windows）
    os.system(f"allure open {allure_report_dir}")